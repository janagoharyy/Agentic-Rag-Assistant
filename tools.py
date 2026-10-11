from smolagents import Tool
from retrieval import semantic_search

#creating a LocalKnowledgeTool that inherets from "Tool" which is provided by smolagents framework
class LocalKnowledgeTool(Tool):
 name="local_knowledge_tool"
 description = (
    "Searches the provided local PDF documents for information. "
    "Use this tool when the user's question is likely answered by the "
    "content of the local documents, especially questions about AI agents, "
    "RAG, and LLMs covered in those documents. "
    "Do not use this tool for information that requires current web data."
)
 inputs={
   "query":{
   "type":"string",
   "description":"A specific question or search query describing the information to find in the local documents."
   }
 } 
 output_type="string"
 def forward(self, query):
        results = semantic_search(query)

        return "\n\n".join(results)
  
   
