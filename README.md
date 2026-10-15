# Agentic RAG Assistant

A tool-calling AI agent built with **smolagents** that combines local PDF retrieval using **LlamaIndex** with web search. The project integrates a custom RAG tool, semantic retrieval, persistent ChromaDB vector storage, Hugging Face embeddings, and a Gradio interface.

The goal is to let the agent retrieve relevant information from local documents or use web search when external information is needed, then generate a response based on the retrieved information.

## Overview

- **Local document retrieval:** Search PDF documents using a custom RAG tool implemented with LlamaIndex.
- **Semantic search:** Retrieve relevant document chunks based on their meaning.
- **Vector storage:** Store document embeddings in a persistent ChromaDB collection.
- **Web search:** Access external information through a web search tool.
- **Tool-calling agent:** Use smolagents to orchestrate tool usage and generate responses.
- **Chat interface:** Interact with the agent through a Gradio interface.

## Demo

### Local RAG Retrieval

The agent retrieves relevant information from the local document collection.

![Local RAG Retrieval Demo](https://github.com/user-attachments/assets/984bc680-6c83-4e87-81ba-949f5a06937b)

### Web Search

The agent uses web search to retrieve external information.

![Web Search Demo](https://github.com/user-attachments/assets/2c536bf7-c77a-4ad3-93df-61b01e89e2b0)

## How It Works

### 1. Local Document Ingestion and Indexing

The RAG pipeline is implemented using LlamaIndex.

- **Document loading:** `SimpleDirectoryReader` loads PDF files from the `documents` directory, using `PyMuPDFReader` for PDF extraction.
- **Chunking:** `SentenceSplitter` divides documents into chunks of 512 tokens with an overlap of 20 tokens.
- **Embedding generation:** `HuggingFaceEmbedding` uses `BAAI/bge-small-en-v1.5` to convert document chunks into vector embeddings.
- **Vector storage:** `ChromaVectorStore` connects LlamaIndex to a persistent ChromaDB collection named `llamaindex_documents`, stored in `./chroma_db_llamaindex`.
- **Ingestion pipeline:** `IngestionPipeline` applies the chunking and embedding transformations and stores the resulting nodes in ChromaDB.

### 2. Semantic Retrieval

When the agent needs information from local documents, its custom RAG tool calls the `search_documents(query)` function.

The function creates a `VectorStoreIndex` from the existing ChromaDB vector store and uses `as_retriever(similarity_top_k=3)` to retrieve the three most relevant document chunks.

The retrieved text is returned to the agent, which uses it to formulate a response. LlamaIndex handles retrieval, while the smolagents agent handles response generation.

### 3. Web Search

A web search tool allows the agent to retrieve information from external sources when appropriate.

### 4. Agent Orchestration

A `ToolCallingAgent` built with smolagents coordinates the available tools, including local document retrieval and web search. The language model is accessed through the Groq API.

### 5. User Interface

A Gradio interface provides a chat-based way to interact with the agent.

## Architecture

```text
User
 |
 v
Gradio Chat Interface
 |
 v
smolagents ToolCallingAgent
 |
 +----------------------+----------------------+
 |                                             |
 v                                             v
Custom RAG Tool                          Web Search Tool
 |                                             |
 v                                             v
LlamaIndex Retriever                   External Information
 |
 v
ChromaDB Vector Store
 |
 v
Top 3 Relevant Document Chunks
 |
 +----------------------+----------------------+
                        |
                        v
                Agent Generates Response
                        |
                        v
                Gradio Chat Interface
```

## Tech Stack

- **Language:** Python
- **Agent framework:** smolagents
- **RAG framework:** LlamaIndex
- **LLM API:** Groq
- **Language model:** Qwen (`qwen/qwen3.8-27b`)
- **Embedding model:** `BAAI/bge-small-en-v1.5` via Hugging Face
- **Vector database:** ChromaDB
- **Document loading:** LlamaIndex `SimpleDirectoryReader` and `PyMuPDFReader`
- **Chunking:** LlamaIndex `SentenceSplitter`
- **Interface:** Gradio
- **Additional tools:** Web search

## Project Structure

Agentic-Rag-Assistant/
├── documents/             # Local PDF documents
├── app.py                 # Gradio interface and agent setup
├── tools.py               # Custom RAG and other agent tools
├── LlamaIndexRAG.py            # LlamaIndex ingestion and retrieval logic
├── main.py                  
├── .env                   # API keys (not committed)
├── .gitignore
└── README.md
## Getting Started

### Prerequisites

- Python 3.12
- A Groq API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/janagoharyy/Agentic-Rag-Assistant.git
cd Agentic-Rag-Assistant
```

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure the dependencies include the LlamaIndex integrations used by the project, including the core package, Hugging Face embeddings, file readers, ChromaDB vector store, and PyMuPDF support.

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not commit your actual API key to GitHub.

### 5. Add Documents

Place the PDF files you want the agent to search in the `documents/` directory.

### 6. Run the Application

```bash
python app.py
```

Follow the terminal output to access the Gradio interface.

## Limitations

- Retrieval quality depends on document content, chunking, embedding quality, and the relevance of the retrieved results.
- Scanned PDFs may require OCR if their text cannot be extracted properly.
- The agent's tool selection and final responses depend on the language model's capabilities.
- Web search results depend on the search provider and the queries generated.
- Persistent storage does not automatically guarantee that documents will be indexed only once; ingestion behavior depends on how the pipeline is executed.

## Future Improvements

- Evaluate retrieval quality using a small set of test questions and expected source passages.
- Add source references to help users verify retrieved information.
- Improve error handling for API failures and tool-call errors.
- Evaluate when the agent should use local retrieval versus web search.
- Prevent duplicate ingestion when rerunning the application.
- Add tests for retrieval accuracy and tool selection.

## What I Learned

- Building a tool-calling agent with smolagents.
- Implementing document ingestion and semantic retrieval with LlamaIndex.
- Using Hugging Face embedding models to represent text as vectors.
- Connecting LlamaIndex to persistent ChromaDB storage.
- Integrating local RAG retrieval and web search within one agent.
- Connecting an AI agent to a Gradio chat interface.

## Status

**Functional learning project** — exploring agentic AI, RAG pipelines, tool integration, and retrieval quality.
