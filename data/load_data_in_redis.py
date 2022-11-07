import asyncio
import pickle
import typing as t

import numpy as np
import redis.asyncio as redis

from config import REDIS_INDEX_TYPE, REDIS_URL
from frontend.lib.query_utils import create_flat_index, create_hnsw_index


def read_paper_df(path_to_pickle_file: str) -> t.List:
    with open(path_to_pickle_file, "rb") as f:
        df = pickle.load(f)
    return df


async def gather_with_concurrency(n, redis_conn, *papers):
    semaphore = asyncio.Semaphore(n)

    async def load_paper(paper):
        async with semaphore:
            vector = paper.pop("vector")
            key = "paper_vector:" + str(paper["id"])
            # async write data to redis
            await redis_conn.hset(
                key,
                mapping={
                    "paper_id": paper["id"],
                    "categories": paper["categories"],
                    "title": paper["title"],
                    "year": paper["year"],
                    "authors": paper["authors"],
                    "abstract": paper["abstract"],
                    "update_date": paper["update_date"],
                    "doi": paper["doi"],
                    "journal-ref": paper["journal-ref"],
                    "submitter": paper["submitter"],
                    "vector": np.array(vector, dtype=np.float32).tobytes(),
                },
            )

    # gather with concurrency
    await asyncio.gather(*[load_paper(p) for p in papers])


async def load_all_data(path_to_pickle_file: str):
    redis_conn = redis.from_url(REDIS_URL)
    if await redis_conn.dbsize() > 300:
        print("papers already loaded")
    else:
        print("Loading papers into Vecsim App")
        papers = read_paper_df(path_to_pickle_file)
        papers = papers.to_dict("records")
        await gather_with_concurrency(100, redis_conn, *papers)
        print("papers loaded!")

        print("Creating vector search index")
        # create a search index
        if REDIS_INDEX_TYPE == "HNSW":
            await create_hnsw_index(redis_conn, len(papers), prefix="paper_vector:", distance_metric="IP")
        else:
            await create_flat_index(redis_conn, len(papers), prefix="paper_vector:", distance_metric="L2")
        print("Search index created")


if __name__ == "__main__":
    embeddings_pickle_file = "data/arxiv_embedings.pkl"
    asyncio.run(load_all_data(path_to_pickle_file=embeddings_pickle_file))
