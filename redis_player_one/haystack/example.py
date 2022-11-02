from redis_player_one.haystack.redis_document_store import RedisDocumentStore
from haystack.nodes.retriever.sparse import BM25Retriever
from haystack.nodes.reader.farm import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from config.redis_config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

document_store = RedisDocumentStore(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False, context_window_size=500)
pipe = ExtractiveQAPipeline(reader, retriever)
prediction = pipe.run(query="What is a VM?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})

print(prediction)
