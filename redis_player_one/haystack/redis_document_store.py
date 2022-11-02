import logging
from typing import List, Optional, Union, Dict

import numpy as np
import redis
from redis.commands.search.query import Query
from haystack.schema import Document


from config.redis_config import INDEX_NAME, SEARCH_TYPE
from haystack.document_stores.search_engine import SearchEngineDocumentStore

from config.redis_config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from redis_player_one.embedder import make_embeddings


logger = logging.getLogger(__name__)


class RedisDocumentStore(SearchEngineDocumentStore):
    def __init__(
        self,
        host: Union[str, List[str]] = "localhost",
        port: Union[int, List[int]] = 9200,
        password: str = "",
        index: str = "document",
        label_index: str = "label",
        search_fields: Union[str, list] = "content",
        content_field: str = "content",
        name_field: str = "name",
        embedding_field: str = "embedding",
        embedding_dim: int = 768,
        custom_mapping: Optional[dict] = None,
        excluded_meta_data: Optional[list] = None,
        analyzer: str = "standard",
        recreate_index: bool = False,
        create_index: bool = False,
        refresh_type: str = "wait_for",
        similarity: str = "dot_product",
        return_embedding: bool = False,
        duplicate_documents: str = "overwrite",
        index_type: str = "flat",
        scroll: str = "1d",
        skip_missing_embeddings: bool = True,
        synonyms: Optional[List] = None,
        synonym_type: str = "synonym",
    ):
        client = self._init_redis_client(host=host, port=port, password=password)

        super().__init__(
            client=client,
            index=index,
            label_index=label_index,
            search_fields=search_fields,
            content_field=content_field,
            name_field=name_field,
            embedding_field=embedding_field,
            embedding_dim=embedding_dim,
            custom_mapping=custom_mapping,
            excluded_meta_data=excluded_meta_data,
            analyzer=analyzer,
            recreate_index=recreate_index,
            create_index=create_index,
            refresh_type=refresh_type,
            similarity=similarity,
            return_embedding=return_embedding,
            duplicate_documents=duplicate_documents,
            index_type=index_type,
            scroll=scroll,
            skip_missing_embeddings=skip_missing_embeddings,
            synonyms=synonyms,
            synonym_type=synonym_type,
        )

        # Let the base class trap the right exception from the redis client
        self._RequestError = redis.exceptions.RedisError

    @classmethod
    def _init_redis_client(
        cls,
        host: str = REDIS_HOST,
        port: str = REDIS_PORT,
        password: str = REDIS_PASSWORD,
    ) -> redis.client.Redis:
        redis_client = redis.Redis(host=host, port=port, password=password)
        return redis_client

    @staticmethod
    def _get_vector_similarity_query(
        categories: list,
        years: list,
        search_type: str = SEARCH_TYPE,
        number_of_results: int = 10,
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
        base_query = f"{tag}=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]"
        # TODO: parametrize vector_score
        return (
            Query(base_query)
            .sort_by("vector_score")
            .paging(0, number_of_results)
            .return_fields(
                "paper_id",
                "vector_score",
                "year",
                "title",
                "authors",
                "abstract",
                "categories",
                "update_date",
                "journal-ref",
                "submitter",
                "doi",
            )
            .dialect(2)
        )

    def retrieve_paper(self, key):
        r_client = self.client
        abstract = r_client.hget(key, "abstract")
        title = r_client.hget(key, "title")
        authors = r_client.hget(key, "authors")
        year = r_client.hget(key, "year")
        paper_id = r_client.hget(key, "paper_id")

        return {
            "abstract": abstract,
            "title": title,
            "authors": authors,
            "year": year,
            "paper_id": paper_id,
        }

    def _create_document_index(self):
        pass

    def _create_label_index(self):
        pass

    def _do_bulk(self):
        pass

    def _do_scan(self):
        pass

    def _get_raw_similarity_score(self, score):
        return score - 1000

    def query_by_embedding(self, query: str, date_range: list, nb_articles: int):
        q = self._get_vector_similarity_query(
            categories=None, years=date_range, search_type=SEARCH_TYPE, number_of_results=nb_articles
        )

        # Vectorize the query
        query_vector = make_embeddings(query).astype(np.float32).tobytes()
        params_dict = {"vec_param": query_vector}

        # Execute the query
        results = self.client.ft(INDEX_NAME).search(q, query_params=params_dict)
        return results

    def query(
        self,
        query: Optional[str],
        filters: Optional[Dict[str, Union[Dict, List, str, int, float, bool]]] = None,
        top_k: int = 10,
        custom_query: Optional[str] = None,
        index: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        all_terms_must_match: bool = False,
        scale_score: bool = True,
    ) -> List[Document]:
        if index is None:
            index = self.index
        date_range = list(map(str, list((range(2016, 2023)))))
        nb_articles = 10
        if isinstance(filters, dict):
            date_range = filters.get("date_range", date_range)
            nb_articles = filters.get("nb_articles", nb_articles)
        results = self.query_by_embedding(query, date_range, nb_articles)

        documents = [self.convert_hit_to_document(hit) for hit in results.docs]
        return documents

    @staticmethod
    def convert_hit_to_document(paper):
        meta_data = {"categories": paper.categories, "title": paper.title, "update_date": paper.update_date}
        doc_dict = {
            "id": paper.paper_id,
            "content": paper.abstract,
            "content_type": "text",
            "meta": meta_data,
            "score": paper.vector_score,
            "embedding": None,
        }
        document = Document.from_dict(doc_dict)
        return document
