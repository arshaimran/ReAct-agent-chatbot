import os
import requests
import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
collection = client["my_rag_db"]["pdf_chunks"]

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embedding function
def embed_query(text):
    return model.encode([text])[0]

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Search top matching chunks from vector DB
def search_similar_chunks(query, top_k=5):
    query_embedding = embed_query(query)
    chunks = list(collection.find({}, {"text": 1, "embedding": 1}))
    
    for c in chunks:
        c["score"] = cosine_similarity(query_embedding, np.array(c["embedding"]))
    
    top_chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)[:top_k]
    return [c["text"] for c in top_chunks]

# Gemini API caller
def call_gemini_with_context(query, context_chunks):
    context = "\n\n".join(context_chunks)
    full_prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer in a clear and concise way."

    data = {"contents": [{"parts": [{"text": full_prompt}]}]}
    url = f"{GEMINI_URL}"
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# RAG Tool Node
def rag_tool_node(state):

    query = state["user_input"]
    print(f"🔍 RAG search for: {query}")

    try:
        chunks = search_similar_chunks(query)
        result = call_gemini_with_context(query, chunks)
        state["result"] = result
        state["history"].append(f"RAG Answer for '{query}': {result}")
    except Exception as e:
        error_msg = f"RAG Tool error: {e}"
        print("❌", error_msg)
        state["result"] = error_msg
        state["history"].append(error_msg)

    return state

# Tavily Tool Node
'''
def tavily_tool_node(state):
    query = state["user_input"]
    print(f"🌐 Tavily search for: {query}")

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "max_results": 3,
        "search_depth": "advanced"
    }

    try:
        response = requests.post("https://api.tavily.com/search", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("🛠️ Tavily raw response:", data)

        results = data.get("results", [])
        if not results:
            result_text = "No results found."
        else:
            summaries = [res.get("content", "") for res in results if "content" in res]
            result_text = "\n\n".join(summaries)

        state["result"] = result_text
        state["history"].append(f"Tavily results for '{query}': {result_text}")

    except Exception as e:
        error_msg = f"Tavily API error: {e}"
        print("❌", error_msg)
        state["result"] = error_msg
        state["history"].append(error_msg)

    return state
    '''

def tavily_tool_node(state):
    query = state["user_input"]
    print(f"🌐 Tavily search for: {query}")

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "max_results": 3,
        "search_depth": "advanced"
    }

    try:
        response = requests.post("https://api.tavily.com/search", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("🛠️ Tavily raw response:", data)

        results = data.get("results", [])
        if not results:
            result_text = "No results found."
        else:
            summaries = [res.get("content", "") for res in results if "content" in res]
            combined_summary = "\n\n".join(summaries)

            # ✂️ Limit to 100 words
            words = combined_summary.split()
            if len(words) > 100:
                result_text = " ".join(words[:100]) + "..."
            else:
                result_text = combined_summary

        state["result"] = result_text
        state["history"].append(f"Tavily results for '{query}': {result_text}")

    except Exception as e:
        error_msg = f"Tavily API error: {e}"
        print("❌", error_msg)
        state["result"] = error_msg
        state["history"].append(error_msg)

    return state
