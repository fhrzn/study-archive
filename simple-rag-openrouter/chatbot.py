from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import logging
import os

logger = logging.getLogger(__file__)


def predict_chat(message, history, model_name):
    prompt = PromptTemplate.from_template(
        "You are an AI assistant that capable to interact with users using friendly tone."
        "Whenever you think it needed, add some emojis to your response. No need to use hashtags."
        "\n\n{message}"
    )

    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE")
    )

    chain = prompt | llm

    ################
    #### STREAM ####
    ################
    partial_msg = ""
    for chunk in chain.stream({"message": message}):
        partial_msg = partial_msg + chunk.content
        yield partial_msg

    ########################
    ##### REGULAR CALL #####
    ########################
    # response = chain.invoke({"message", message})
    # yield response.content
    