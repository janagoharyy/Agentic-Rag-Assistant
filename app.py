import gradio as gr #gradio is a python library that lets u create web interface for ur python program
print("APP STARTED")
from main import agent
print("2. Agent imported")

def chat(message,history):
    response=agent.run(message)
    return str(response)

demo=gr.ChatInterface(  #Creating chat interface object
    fn=chat,
    title="Agentic RAG Assistant",
    description="Ask questions about your documents or search the web"
)
print("3. Launching Gradio")
demo.launch()