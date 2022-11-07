import streamlit as st
import torch
from haystack.nodes import EmbeddingRetriever
from haystack.nodes.reader.farm import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from redis.asyncio import Redis
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from askyves.redis_document_store import RedisDocumentStore
from config import INDEX_NAME, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, TOP_K_READER, TOP_K_RETRIEVER


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


async def create_index(redis_conn, prefix: str, v_field: VectorField):
    categories_field = TagField("categories")
    year_field = TagField("year")
    # Create Index
    await redis_conn.ft(INDEX_NAME).create_index(
        fields=[v_field, categories_field, year_field],
        definition=IndexDefinition(prefix=[prefix], index_type=IndexType.HASH),
    )


async def create_flat_index(redis_conn: Redis, number_of_vectors: int, prefix: str, distance_metric: str = "L2"):
    text_field = VectorField(
        "vector",
        "FLAT",
        {
            "TYPE": "FLOAT32",
            "DIM": 768,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
            "BLOCK_SIZE": number_of_vectors,
        },
    )
    await create_index(redis_conn, prefix, text_field)


async def create_hnsw_index(redis_conn: Redis, number_of_vectors: int, prefix: str, distance_metric: str = "COSINE"):
    text_field = VectorField(
        "vector",
        "HNSW",
        {
            "TYPE": "FLOAT32",
            "DIM": 768,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
        },
    )
    await create_index(redis_conn, prefix, text_field)
