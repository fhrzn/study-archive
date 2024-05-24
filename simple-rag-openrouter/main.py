import gradio as gr
from dotenv import load_dotenv
import logging
from chatbot import predict_chat
import httpx

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(name)s - %(message)s")
logger = logging.getLogger(__file__)


def get_free_models():
    res = httpx.get("https://openrouter.ai/api/v1/models")
    if res:
        res = res.json()
        models = [item["id"] for item in res["data"] if "free" in item["id"]]
        return models


with gr.Blocks(fill_height=True) as demo:

    models = get_free_models()
    
    model_choice = gr.Dropdown(
        choices=models,
        show_label=True,
        label="Model Choice",
        interactive=True,
        value=models[0]
    )

    chat_window = gr.Chatbot(bubble_full_width=False, render=False, scale=1)

    chat = gr.ChatInterface(
        predict_chat,
        chatbot=chat_window,
        additional_inputs=model_choice,
        fill_height=True,
        retry_btn=None,
        undo_btn=None,
        clear_btn=None
    )

    

if __name__ == "__main__":
    demo.queue()
    demo.launch()