from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.callbacks.tracers import ConsoleCallbackHandler
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)


def get_chat_history(session_id: str, limit: Optional[int] = None):
    chat_history = SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///memory.db")
    if limit:
        chat_history.messages = chat_history.messages[-limit:]

    return chat_history


def predict_chat(message: str, history: list, model_name: str, user_id: str):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant that capable to interact with users using friendly tone. Whenever you think it needed, add some emojis to your response. No need to use hashtags."),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE")
    )

    chain = prompt | llm

    history_runnable = RunnableWithMessageHistory(
        chain,
        get_session_history=get_chat_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    ################
    #### STREAM ####
    ################
    partial_msg = ""
    # for chunk in chain.stream({"message": message}):
    for chunk in history_runnable.stream({"input": message}, config={"configurable": {"session_id": user_id}, "callbacks": [ConsoleCallbackHandler()]}):
        partial_msg = partial_msg + chunk.content
        yield partial_msg

    ########################
    ##### REGULAR CALL #####
    ########################
    # response = chain.invoke({"message", message})
    # yield response.content
