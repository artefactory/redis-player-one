# Get data from Kaggle

- You can download the Arxiv dataset from here:
    - https://www.kaggle.com/datasets/Cornell-University/arxiv

- (Recommended solution) If you have a Kaggle account:
    - go to your account and create an API key
    - put the created key in `~/.kaggle/kaggle.json`
    - then use the CLI to download the dataset:
        - `kaggle datasets download -d Cornell-University/arxiv`


# Build embeddings

- Run through the `build_embeddings_multi_gpu.ipynb` notebook on Saturn Cloud (Jupyter server + Dask Cluster) to build the embeddings.

# Load data to Redis

- Once the embeddings built:
    - You'll need to export env variable. Check `credentials/env.sh.exemple` to have the list    
    - Then, run `python data/load_data_in_redis.py`