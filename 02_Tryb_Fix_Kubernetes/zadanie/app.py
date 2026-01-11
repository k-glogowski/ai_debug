import gradio as gr
import os 
from dotenv import load_dotenv
load_dotenv()

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch(server_name=os.getenv("GRADIO_SERVER_NAME"), server_port=int(os.getenv("GRADIO_SERVER_PORT")))