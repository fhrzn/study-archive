import os
import sys
from dotenv import load_dotenv

from langchain_openai.chat_models.azure import AzureChatOpenAI
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_community.document_loaders.wikipedia import WikipediaLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.llm import LLMChain

from langfuse.callback import CallbackHandler
from langfuse import Langfuse

load_dotenv()



def setup_langfuse():
    print("setup langfuse...")
    # analytics
    langfuse_callback = CallbackHandler(
        secret_key="sk-lf-d26600a7-aa86-4aae-af39-e09c0155a96d",
        public_key="pk-lf-aaa63774-ad52-487e-9e2f-1f354b0d60ae",
        host="http://localhost:3000",
        tags=["RAG"]
    )

    return langfuse_callback


def init_models():
    print("init model...")
    # LLM & Embedding
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    )

    embedding = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    )

    return llm, embedding


def ingest_data(query: str, embedding: AzureOpenAIEmbeddings, lang: str = "id"):
    print("ingesting data...")
    # document loader
    loader = WikipediaLoader(query=query, lang=lang, load_max_docs=3)
    docs = loader.load()
    vectorstores = FAISS.from_documents(docs, embedding)

    return vectorstores


def retrieval_mode(question: str, wiki_search: str, llm: AzureChatOpenAI, embedding: AzureOpenAIEmbeddings, langfuse_handler: CallbackHandler):
    # get vectorstore
    vectorstore = ingest_data(wiki_search, embedding)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    # setup prompt
    prompt_str = (
        "Use the given context to answer the question. \n"
        "If you don't know the answer, say you don't know. \n"
        "Use three sentence maximum and keep the answer concise.\n"
        "-------------------------------------------------------\n"
        "Context: ```\n{context}\n````\n"
        "-------------------------------------------------------\n"
        "Question: \"{question}\""
    )    
    prompt = PromptTemplate.from_template(prompt_str)

    retrieval_chain = RetrievalQA.from_llm(llm, prompt, retriever=retriever, llm_chain_kwargs={"verbose": True})
    result = retrieval_chain.run({"query": question}, callbacks=[langfuse_handler])

    return result


# OPTIONAL
def general_mode(question: str, llm: AzureChatOpenAI, langfuse_handler: CallbackHandler):
    prompt = PromptTemplate.from_template("Answer the given question below\n Question: {text}")
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.predict(text=question, callbacks=[langfuse_handler])
    return result


if __name__ == "__main__":

    # init model
    llm, embedding = init_models()

    # langfuse
    langfuse_handler = setup_langfuse()

    try:
        while True:
            wiki_search = input("Enter wikipedia keyword (optional): ")
            question = input("Enter your question: ")

            result = retrieval_mode(question, wiki_search, llm, embedding, langfuse_handler)
            print(result)
    except KeyboardInterrupt:
        print()
        sys.exit(1)
