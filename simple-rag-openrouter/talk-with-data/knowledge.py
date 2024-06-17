from pymilvus import MilvusClient, model
from typing import Union, List, Optional
import logging
import re
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import gradio as gr
import os
import time
from langchain_core.messages.base import BaseMessage
from langchain_core.messages import SystemMessage


logger = logging.getLogger(__file__)


MILVUS = None

def init_vectordb(path: Optional[str] = None):
    if not path:
        path = os.getenv("MILVUS_DB_PATH")

    global MILVUS
    if not MILVUS:
        logger.info("initiating vectordb")
        MILVUS = MilvusClient(path)


def close_vectordb():
    if MILVUS:
        logger.info("closing vectordb")
        MILVUS.close()


def upload_file(collection_name: str, file: Union[str, list[str], None]):

    start_upload = time.time()

    re_ptn = r'((\w+?\-)+)?\w+\.(csv|pdf|txt)'
    filename = re.search(re_ptn, file).group()
    extension = filename.split('.')[-1]

    if extension == 'csv':
        loader = CSVLoader(file)
        data = loader.load()
    elif extension == 'pdf':
        loader = PyPDFLoader(file)
        data = loader.load()
        splitter = RecursiveCharacterTextSplitter()
        data = splitter.split_documents(data)
    else:
        raise NotImplementedError(f"Loader for {extension} not implemented yet.")

    __encode_and_insert(MILVUS, data, collection_name)

    # re-retrieve all collection_name to update the dropdown
    collections = get_collections()

    logger.info(f"Time elapsed {time.time() - start_upload:.1f}s | Collection name: {collection_name}")

    return [
        gr.Textbox(value=None),
        gr.File(value=None),
        gr.Dropdown(choices=collections, interactive=True, value=collections[0]),
        gr.Tabs(selected="chat")
    ]
    

def __encode_and_insert(client: MilvusClient, data: List[Document], collection_name: str):
    # extract content
    content = [item.page_content for item in data]

    # encode content to vector
    embedding_fn = model.DefaultEmbeddingFunction()
    vectors = embedding_fn.encode_documents(content)

    data = [{"id": i, "vector": vectors[i], **data[i].dict()} for i in range(len(vectors))]

    client.create_collection(
        collection_name=collection_name,
        dimension=embedding_fn.dim,
        # auto_id=True
    )
    
    client.insert(collection_name=collection_name, data=data)


def get_collections():
    init_vectordb()
    collections = MILVUS.list_collections()
    return collections


def query(query: str, collection_name: str):
    query_str = query
    if isinstance(query, dict) and "input" in query:
        query_str = query["input"]

    start_query = time.time()
    embedding_fn = model.DefaultEmbeddingFunction()
    query_vector = embedding_fn.encode_queries([query_str])

    result = MILVUS.search(
        collection_name=collection_name,
        data=query_vector,
        output_fields=[
            "page_content"
        ],
        limit=1000
    )

    logger.info(f"Time elapsed: {time.time() - start_query:.1f}s | Query: \"{query_str}\"")

    context_str = ""
    for res in result:
        for r in res:
            context_str += r['entity']['page_content'] + "\n"
    
    # query["context"] = context_str
    return context_str
    # return [SystemMessage(context_str)]
    # return SystemMessage(context_str)
