import os
from pathlib import Path
import torch


def get_project_root() -> Path:
    return Path(__file__).parent.parent


# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "NONE__REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", "NONE__REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "NONE__REDIS_PASSWORD")
REDIS_DB = os.environ.get("REDIS_DB", "NONE__REDIS_DB")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
INDEX_NAME = "papers"

missing = [
    env_var.lstrip("NONE__")
    for env_var in [REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB]
    if env_var.startswith("NONE__")
]
if missing:
    raise RuntimeError(f"The following env variables haven't been set : {missing}")

SEARCH_TYPE = "KNN"
NUMBER_OF_RESULTS = 10
ROOT_PATH = get_project_root()

if torch.cuda.is_available():
    TOP_K_RETRIEVER = 100
else:
    TOP_K_RETRIEVER = 10

TOP_K_READER = 10
