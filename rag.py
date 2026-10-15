from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import asyncio
import chromadb

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore


# Create a reader that looks inside the documents folder
reader = SimpleDirectoryReader(input_dir="documents",file_extractor={".pdf": PyMuPDFReader()})

# load data method loads all files in that folder into a list of Document objects
documents = reader.load_data()

# Create the embedding model that converts chunks into numerical vectors
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Connect to a persistent ChromaDB database
# The data will be saved in this folder instead of existing only in memory
db = chromadb.PersistentClient(path="./chroma_db_llamaindex")

# Create or access a collection inside ChromaDB
chroma_collection = db.get_or_create_collection(
    name="llamaindex_documents"
)

# Connect LlamaIndex to the ChromaDB collection
vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)

# IngestionPipeline packages the steps into a reusable pipeline.
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(
            chunk_overlap=20,
            chunk_size=512
        ),  # here chunking creates chunks of 512 tokens, not 512 characters
        embed_model
    ],
    vector_store=vector_store #VectorStoreIndex as the thing that organizes your document chunks so you can search them by meaning. 
)

# Using the async method arun to run the pipeline and return a list of nodes
async def main():
    nodes = await pipeline.arun(documents=documents)
    print(f"Processed {len(nodes)} nodes")

    # Create an index connected to the vectors stored in ChromaDB
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )

    print("VectorStoreIndex connected to ChromaDB successfully")
    print(f"Chunks stored in ChromaDB: {chroma_collection.count()}")
    retriever = index.as_retriever()
#as_retriever() finds relevant information- as_query_engine() finds information and generates an answer
#since ill already integrate it with smolagents agent i dont need it to generate answer
    # Test retrieval without generating an answer
    retrieved_nodes = retriever.retrieve("What is RAG?")

    for i, node in enumerate(retrieved_nodes, start=1):
        print(f"\nRetrieved chunk {i}:")
        print(node.text)


asyncio.run(main())