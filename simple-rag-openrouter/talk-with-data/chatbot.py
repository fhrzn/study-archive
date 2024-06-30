from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.callbacks.tracers import ConsoleCallbackHandler
from typing import Optional
import logging
import os
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import knowledge
from functools import partial

logger = logging.getLogger(__name__)


def get_chat_history(session_id: str, limit: Optional[int] = None, **kwargs):
    if isinstance(session_id, dict) and "session_id" in session_id:
        session_id = session_id["session_id"]

    chat_history = SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///memory.db")
    if limit:
        chat_history.messages = chat_history.messages[-limit:]

    return chat_history


def predict_chat(message: str, history: list, model_name: str, user_id: str, collection_name: str):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant that capable to interact with users using friendly tone. "
         "Whenever you think it needed, add some emojis to your response. No need to use hashtags."
         "\n\n"
         "Answer user's query based on the following context:\n"
         "{context}"
         "\n---------------\n"
         "Chat history:\n"),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ])

    # Optionally, you may use this format as well
    # prompt = ChatPromptTemplate.from_template(
    #     'You are an AI assistant that capable to interact with users using friendly tone.'
    #     'Whenever you think it needed, add some emojis to your response. No need to use hashtags.'
    #     '\n\n'
    #     'Answer user\'s input based on the following context below. If the context doesn\'t contains'
    #     'the suitable answers, just say you dont know. Dont make up the answer!\n'
    #     '{context}'
    #     '\n---------------\n'
    #     'Chat history:\n'
    #     '{history}'
    #     '\n---------------\n'
    #     'User input: {input}'
    # )

    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE")
    )

    # runnable for retrieving knowledge
    query_runnable = RunnableLambda(partial(knowledge.query, collection_name=collection_name))

    # ##### FOR DEBUGGING ONLY #####
    # _context = query_runnable.invoke(input=message)
    # logger.info(f"context: {_context}")

    chain = (
        RunnablePassthrough.assign(context=query_runnable)
        | prompt
        | llm
    )

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
    for chunk in history_runnable.stream({"input": message}, config={"configurable": {"session_id": user_id}, "callbacks": [ConsoleCallbackHandler()]}):
        partial_msg = partial_msg + chunk.content
        yield partial_msg

    ########################
    ##### REGULAR CALL #####
    ########################
    # response = chain.invoke({"input": message, "session_id": user_id}, config={"callbacks": [ConsoleCallbackHandler()]})
    # yield response.content
