import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

# Load JSON files
with open("../data/text_chunks.json", "r", encoding="utf-8") as f:
    text_chunks = json.load(f)

with open("../data/table_chunks.json", "r", encoding="utf-8") as f:
    table_chunks = json.load(f)

# Initialize ChromaDB
client = chromadb.PersistentClient(path="../data/chroma_db")  # folder where DB is stored
collection = client.get_or_create_collection(name="medical_chunks")

# Initialize embedding model
model = SentenceTransformer("intfloat/multilingual-e5-base")

# Prepare and add text chunks
for i, chunk in enumerate(text_chunks):
    embedding = model.encode(chunk["content"])
    collection.add(
        ids=[f"text_{i}"],
        metadatas=[{
            "title": chunk["title"],
            "page": chunk["page"],
            "domain": chunk.get("domain", "")
        }],
        documents=[chunk["content"]],
        embeddings=[embedding.tolist()]
    )

# Prepare and add table chunks (flatten rows to text)
for i, table in enumerate(table_chunks):
    for j, row in enumerate(table.get("row", {}).values()):
        if isinstance(row, str):
            embedding = model.encode(row)
            collection.add(
                ids=[f"table_{i}_{j}"],
                metadatas=[{"table_id": table.get("table_id")}],
                documents=[row],
                embeddings=[embedding.tolist()]
            )

print("All chunks embedded and stored in ChromaDB ✅")