import numpy as np
import streamlit as st
from redis.commands.search.query import Query

from haystack.nodes import EmbeddingRetriever
from haystack.nodes.reader.farm import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
import torch

from redis_player_one.haystack.redis_document_store import RedisDocumentStore
from config.redis_config import INDEX_NAME, SEARCH_TYPE, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, TOP_K_RETRIEVER, TOP_K_READER
from redis_player_one.embedder import make_embeddings
from redis_player_one.redis_client import redis_client


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
            model_name_or_path="deepset/roberta-base-squad2", use_gpu=torch.cuda.is_available(), context_window_size=2000)
        pipe = ExtractiveQAPipeline(reader, retriever)
    return pipe



def create_query(
    categories: list,
    years: list,
    search_type: str = SEARCH_TYPE,
    number_of_results: int = 10
) -> Query:
    tag = "("
    if years:
        years = " | ".join(years)
        tag += f"@year:{{{years}}}"
    if categories:
        categories = " | ".join(categories)
        tag += f"@categories:{{{categories}}}"
    tag += ")"
    # if no tags are selected
    if len(tag) < 3:
        tag = "*"
    print(tag, flush=True)
    base_query = f'{tag}=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]'
    return Query(base_query)\
        .sort_by("vector_score")\
        .paging(0, number_of_results)\
        .return_fields("paper_id",
                       "vector",
                       "vector_score",
                       "year",
                       "title",
                       "authors",
                       "abstract",
                       "categories",
                       "update_date",
                       "journal-ref",
                       "submitter",
                       "doi")\
        .dialect(2)


def query_redis(text: str, date_range: list, nb_articles: int):    # TODO: Delete if not used
    q = create_query(categories=None,
                     years=date_range,
                     search_type=SEARCH_TYPE,
                     number_of_results=nb_articles)

    # Vectorize the query
    query_vector = make_embeddings(text).astype(np.float32).tobytes()
    params_dict = {"vec_param": query_vector}

    # Execute the query
    results = redis_client.ft(INDEX_NAME).search(q, query_params=params_dict)
    return results


def make_qa_query(pipe, text: str, date_range: list):
    results = pipe.run(
        query=text,
        params={
            "Retriever": {"top_k": TOP_K_RETRIEVER, "filters": {"date_range": date_range}},
            "Reader": {"top_k": TOP_K_READER}},
        debug=True)
    return results