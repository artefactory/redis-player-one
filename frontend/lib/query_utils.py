import streamlit as st
import torch
from haystack.nodes import EmbeddingRetriever
from haystack.nodes.reader.farm import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

from askyves.redis_document_store import RedisDocumentStore
from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, TOP_K_READER, TOP_K_RETRIEVER


@st.experimental_singleton(show_spinner=False)
def instanciate_retriever():
    with st.spinner("Loading models..."):
        document_store = RedisDocumentStore(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        retriever = EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/all-mpnet-base-v2",
            model_format="sentence_transformers",
        )
        reader = FARMReader(
            model_name_or_path="deepset/roberta-base-squad2",
            use_gpu=torch.cuda.is_available(),
            context_window_size=2000,
        )
        pipe = ExtractiveQAPipeline(reader, retriever)
    return pipe


def make_qa_query(pipe, text: str, date_range: list):
    results = pipe.run(
        query=text,
        params={
            "Retriever": {"top_k": TOP_K_RETRIEVER, "filters": {"date_range": date_range}},
            "Reader": {"top_k": TOP_K_READER},
        },
        debug=True,
    )
    return results
