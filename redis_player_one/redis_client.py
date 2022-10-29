import redis
from redis_conf import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


def retrieve_paper(r_client, key):
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
        "paper_id": paper_id
    }
