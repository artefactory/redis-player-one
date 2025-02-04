import os
from pathlib import Path

import torch


def get_project_root() -> Path:
    return Path(__file__).parent


# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "NONE__REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", "NONE__REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "NONE__REDIS_PASSWORD")
REDIS_DB = os.environ.get("REDIS_DB", "NONE__REDIS_DB")
REDIS_INDEX_TYPE = os.environ.get("REDIS_DB", "NONE__REDIS_INDEX_TYPE")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
INDEX_NAME = "papers"

missing = [
    env_var.lstrip("NONE__")
    for env_var in [REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_INDEX_TYPE]
    if env_var.startswith("NONE__")
]
if missing:
    raise RuntimeError(f"The following env variables haven't been set : {missing}")

SEARCH_TYPE = "KNN"
NUMBER_OF_RESULTS = 10

ROOT_PATH = get_project_root()
ASKYVES_IMG_PATH = str(ROOT_PATH / "assets/askyves.png")
REDIS_ICON_PATH = "https://arxiv.org/favicon.ico"

FONT_AWESOME_IMPORT = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'  # noqa: E501

if torch.cuda.is_available():
    TOP_K_READER = 100
else:
    TOP_K_READER = 10

TOP_K_RETRIEVER = 10
