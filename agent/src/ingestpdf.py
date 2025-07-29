from pymongo import MongoClient
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["my_rag_db"]
collection = db["pdf_chunks"]

# Clear old data
collection.delete_many({})

# Load PDF (✅ put your actual path here)
loader = PyPDFLoader(r"C:\Users\arsha\OneDrive\Desktop\reAct\agent\netsol_2023_annualreport.pdf")
pages = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

# Embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Insert into MongoDB
for chunk in chunks:
    embedding = model.encode([chunk.page_content])[0].tolist()
    collection.insert_one({
        "text": chunk.page_content,
        "embedding": embedding
    })

print(f"✅ Ingested {len(chunks)} chunks into MongoDB.")
