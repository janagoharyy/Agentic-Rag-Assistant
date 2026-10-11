# THE RAG SYSTEM

from pypdf import PdfReader
import chromadb
from pathlib import Path
import requests
import re

#we will use this function to clean the text extracted from the PDF documents, removing noise, special characters, and extra whitespace.
def clean_text(text):

    # Remove excessive whitespace
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue # Skip empty lines

        if line.startswith("Page "):
            continue # Skip page numbers
        if line.startswith("Table of Contents"):
            continue # Skip table of contents
        if line.isdigit():
            continue # Skip lines that are just numbers
        # Skip TOC entries with dotted leaders + page number
        if re.search(r"\.{3,}\s*\d+\s*$", line):
            continue


        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


#1) FIND TEXT
documents = Path("documents").glob("*.pdf")
chunks = []

for doc in documents:

    reader = PdfReader(doc)  #2) READ & EXTRACT TEXT

    #3) CONVERT TEXT TO PYTHON STRING
    text = ""

    for page in reader.pages:
        page_text= page.extract_text()
        if page_text: #protection if page has no extractable text
            text += page_text+"\n"  #\n protects page boundaries 

    #clean text from noise, special characters, and extra whitespace
    text = clean_text(text)
    #4) FIXED CHUNKING
    chunk_size = 800
    overlap = 150
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap


#5) EMBEDDING FUNCTION
def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        }
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]


#6) BUILD DATABASE
def build_database():

    embeddings = [get_embedding(chunk) for chunk in chunks]

    client = chromadb.PersistentClient(path="./chroma_db")

    collection = client.get_or_create_collection(
        name="pdf_documents_ollama"
    )

    collection.upsert(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings
    )

    return collection


#7) CHROMA DB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="pdf_documents_ollama"
)


#8) SEMANTIC SEARCH
def semantic_search(query, n_results=3):

    #1) Embed input
    query_embedding = get_embedding(query)

    #2) Find closest embeddings
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    #3) Return selected documents
    return results["documents"][0]