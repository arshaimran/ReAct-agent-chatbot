import requests
from db import collection
import re



TAVILY_API_KEY = "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"



def rag_tool_node(state):
    query_year = None
    user_input = state["user_input"].lower()

    # try to extract year from query
    for y in [2023, 2024, 2025]:
        if str(y) in user_input:
            query_year = y
            break

    # find documents
    query = {"company": "Netsol"}
    if query_year:
        query["year"] = query_year

    docs = collection.find(query)

    results = []
    for doc in docs:
        year = doc.get("year")
        quarter = doc.get("quarter")
        report = doc.get("report")
        results.append(f"Year: {year} | Quarter: {quarter} | Report: {report}")

    if not results:
        state["result"] = "No financial data found."
    else:
        state["result"] = "\n".join(results)

    state["history"].append(state["result"])
    return state


def tavily_tool_node(state):
    query = state["user_input"]
    print(f"🌐 Tavily search for: {query}")

    url = "https://api.tavily.com/search"
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
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("🛠️ Tavily raw response:", data)

        results = data.get("results", [])
        if not results:
            result_text = "No results found."
        else:
            # ✅ use "content" field instead of "snippet"
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

