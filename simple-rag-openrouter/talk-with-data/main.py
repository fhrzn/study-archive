import gradio as gr
from dotenv import load_dotenv
import logging
from chatbot import predict_chat
import knowledge
import httpx
import uuid

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(filename)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)


# MILVUS_CLIENT = None


def get_free_models():
    res = httpx.get("https://openrouter.ai/api/v1/models")
    if res:
        res = res.json()
        models = [item["id"] for item in res["data"] if "free" in item["id"]]
        return sorted(models)

with gr.Blocks(fill_height=True) as demo:
        
    with gr.Tabs() as tabs:
        with gr.TabItem("Chat", id="chat"):
            models = get_free_models()
            collections = knowledge.get_collections()
                
            user_ids = gr.Textbox(visible=False, value=uuid.uuid4())

            with gr.Row():
                model_choice = gr.Dropdown(
                    choices=models,
                    show_label=True,
                    label="Model Choice",
                    interactive=True,
                    value=models[0],
                )

                collection_list = gr.Dropdown(
                    choices=collections,
                    label="VectorDB Collection",
                    interactive=True,
                    value=collections[0] if collections else None
                )

            chat_window = gr.Chatbot(bubble_full_width=False, render=False, scale=1, height=600)

            chat = gr.ChatInterface(
                predict_chat,
                chatbot=chat_window,
                additional_inputs=[model_choice, user_ids, collection_list],
                fill_height=True,
                retry_btn=None,
                undo_btn=None,
                clear_btn=None
            )

        with gr.TabItem("Knowledge", id="knowledge"):
            collection_name = gr.Textbox(label="Collection Name")
            upfile = gr.File(label="Upload File")
            submit_file = gr.Button("Submit Knowledge", variant="primary")
        
        submit_file.click(knowledge.upload_file, inputs=[collection_name, upfile], outputs=[collection_name, upfile, collection_list, tabs])


    demo.load(lambda: knowledge.get_collections())

    

if __name__ == "__main__":
    demo.queue()
    demo.launch()
    
    