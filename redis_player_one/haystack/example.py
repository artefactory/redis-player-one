from haystack.nodes import DensePassageRetriever, RAGenerator
from haystack.pipelines import GenerativeQAPipeline  # ExtractiveQAPipeline
from haystack.utils import print_answers

from config.redis_config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from redis_player_one.haystack.redis_document_store import RedisDocumentStore

document_store = RedisDocumentStore(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

QUESTION = "What are the symptoms of coronavirus ?"

# Exctractive
# retriever = EmbeddingRetriever(
#     document_store=document_store,
#     embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
#     model_format="sentence_transformers",
# )
# reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False, context_window_size=2000)
# pipe = ExtractiveQAPipeline(reader, retriever)
# prediction = pipe.run(
#     query=QUESTION,
#     params={
#         "Retriever": {"top_k": 10, "filters": {"date_range": ["2019", "2020", "2021", "2022"]}},
#         "Reader": {"top_k": 10},
#     },
#     debug=True,
# )
# documents = prediction["documents"]


# Generative
dpr_retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
)
rag_generator = RAGenerator(
    model_name_or_path="facebook/rag-token-nq",
    use_gpu=True,
    top_k=1,
    max_length=200,
    min_length=2,
    embed_title=True,
    num_beams=2,
)
pipe = GenerativeQAPipeline(generator=rag_generator, retriever=dpr_retriever)
result = pipe.run(query=QUESTION, params={"Generator": {"top_k": 1}, "Retriever": {"top_k": 5}})
print_answers(result, max_text_len=200)
