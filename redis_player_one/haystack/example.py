from redis_player_one.haystack.redis_document_store import RedisDocumentStore
from haystack.nodes.retriever.sparse import BM25Retriever
#from haystack.nodes import EmbeddingRetriever
from haystack.nodes.reader.farm import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_documents, print_answers

from config.redis_config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

document_store = RedisDocumentStore(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
# retriever = EmbeddingRetriever(
#     document_store=document_store,
#     embedding_model="sentence-transformers/all-mpnet-base-v2",
#     model_format="sentence_transformers")
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False, context_window_size=2000)
pipe = ExtractiveQAPipeline(reader, retriever)
prediction = pipe.run(
    query="What are the main causes of road accidents and traffic jam ?",
    params={
        "Retriever": {"top_k": 10, "filters": {"date_range": ["2019", "2020", "2021", "2022"]}},
        "Reader": {"top_k": 1}},
    debug=True)
print_documents(prediction, max_text_len=200)
print_answers(prediction, max_text_len=200)
