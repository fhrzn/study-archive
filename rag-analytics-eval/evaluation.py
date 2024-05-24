from langfuse import Langfuse
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain.chat_models.azure_openai import AzureChatOpenAI
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
import pandas as pd
from typing import List

load_dotenv()


def init_models():
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


def get_traces_dataset(langfuse_client: Langfuse, tag: str):
    # get traces
    response = langfuse_client.client.trace.list(tags=tag)
    traces = response.data
    
    evaluation_set = {
        "question": [],
        "contexts": [],
        "answer": [],
        "trace_id": []
    }

    # extract question, context, answer
    for t in traces:
        observations = [langfuse_client.client.observations.get(o) for o in t.observations]
        for o in observations:
            if o.name == "LLMChain":
                question = o.input["question"]
                contexts = [o.input["context"]]
                answer = o.output["text"]
        
        evaluation_set['question'].append(question)
        evaluation_set['contexts'].append(contexts)
        evaluation_set['answer'].append(answer)
        evaluation_set['trace_id'].append(t.id)

    return evaluation_set


def ingest_score(langfuse_client: Langfuse, scores: pd.DataFrame, metric_names: List[str]):
    for _, row in scores.iterrows():
        for metric in metric_names:
            langfuse_client.score(
                name=metric,
                value=row[metric],
                trace_id=row["trace_id"]
            )





if __name__ == "__main__":
    # init
    langfuse = Langfuse(
        secret_key="sk-lf-d26600a7-aa86-4aae-af39-e09c0155a96d",
        public_key="pk-lf-aaa63774-ad52-487e-9e2f-1f354b0d60ae",
        host="http://localhost:3000",
    )

    llm, embedding = init_models()

    # get dataset
    evaluation_set = get_traces_dataset(langfuse, tag="RAG")
    evaluation_set = Dataset.from_dict(evaluation_set)

    # evaluate
    scores = evaluate(evaluation_set,
                      metrics=[faithfulness, answer_relevancy],
                      llm=llm,
                      embeddings=embedding,
                      raise_exceptions=False)
    
    scores = scores.to_pandas()

    # save result
    ingest_score(langfuse, scores, metric_names=["faithfulness", "answer_relevancy"])