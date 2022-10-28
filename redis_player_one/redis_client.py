import os
import redis

R_HOST = os.getenv("R_HOST")
R_PORT = os.getenv("R_PORT")
R_PASSWORD = os.getenv("R_PASSWORD")

redis_client = redis.Redis(host=R_HOST, port=R_PORT, password=R_PASSWORD)


def retrieve_paper(r_client, key):
    abstract = r_client.hget(key, "abstract")
    title = r_client.hget(key, "title")
    authors = r_client.hget(key, "authors")
    year = r_client.hget(key, "year")

    return {
        "abstract": abstract,
        "title": title,
        "authors": authors,
        "year": year,
    }

