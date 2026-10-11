import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, OpenAIModel, WebSearchTool
from tools import LocalKnowledgeTool

load_dotenv()

local_knowledge_tool = LocalKnowledgeTool()
websearchtool = WebSearchTool(engine="bing") #instantiating the toolfrom its class in smolagents framework

model = OpenAIModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

with open("instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

agent = ToolCallingAgent(
    model=model,
    tools=[websearchtool, local_knowledge_tool],
    max_steps=6,
    instructions=instructions,
)