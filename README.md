
# **Ask' Yves**
<div align="center">
    <a href="https://pd-redis-redisplay-ea87d28003b046a8a3617ebdbddfdbe3.community.saturnenterprise.io/"><img src="assets/askyves.png" width="50%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://hackathon.redisventures.com/"><b>Hackathon Page</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://www.kaggle.com/datasets/Cornell-University/arxiv"><b>ArXiv dataset</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://pd-redis-redisplay-ea87d28003b046a8a3617ebdbddfdbe3.community.saturnenterprise.io/"><b>Hosted App</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>


Yves Saint Laurent was one of the greatest minds of french history. He spent a lot of time reading scientific papers on arXiv.

Ask him anything. He will have an answer. Probably not the right one, but you might be surprised 😅


# **How to use the app**
![Ask'Yves app interface](assets/app_interface.png)

Ask'Yves app allows you to ask questions to Yves, who will search for an answer in abstracts of the ArXiv database. Whenever he has found something, Yves will display a set of abstracts ranked by relevance, and highlight the answer to your question in the abstract text.

To ask a question to Yves, just fill the text prompt window on the left sidebar, select a range of publication dates to retrieve abstracts from, and click on "Ask Yves". The results will then be displayed along with information regarding the abstract: 
- Relevance score
- Publication date
- Categories

You can then access the article on arXiv by directly clicking on the article's title.

# **How to setup the app**

## **File architecture**
```
.
├── LICENSE
├── Makefile
├── README.md
├── askyves
│   ├── embedder.py
│   └── redis_document_store.py
├── assets
│   ├── app_interface.png
│   ├── askyves.png
│   └── categories.py
├── config.py
├── credentials
│   ├── env.sh.example
├── data
│   ├── README.md
│   ├── build_embeddings_multi_gpu.ipynb
│   ├── load_data_in_redis.py
│   └── requirements.txt
├── frontend
│   ├── lib
│   │   ├── __init__.py
│   │   ├── app_utils.py
│   │   └── query_utils.py
│   └── streamlit_app.py
├── pyproject.toml
├── requirements.in
├── requirements.txt
└── saturn-deployment-recipe.json
```

Project is divided into multiple folders:
- askyves/ contains files related to document embedding and document store definition
- data/ contains files related to Redis Database creation
- frontend/ contains files related to the Streamlit App

To setup the app, you'll first need to create a Redis DB containing your embedded documents. You'll then be able to launch and use the app, locally or on a Saturn Cloud instance.

## **Data and database**

### Get data from Kaggle

- You can download the Arxiv dataset from here:
    - https://www.kaggle.com/datasets/Cornell-University/arxiv

- (Recommended solution) If you have a Kaggle account:
    - go to your account and create an API key
    - put the created key in `~/.kaggle/kaggle.json`
    - then use the CLI to download the dataset:
        - `kaggle datasets download -d Cornell-University/arxiv`


### Build embeddings

- Run through the `build_embeddings_multi_gpu.ipynb` notebook on Saturn Cloud (Jupyter server + Dask Cluster) to build the embeddings.

### Load data to Redis

- Once the embeddings are built:
    - You'll need to export env variables. Check `credentials/env.sh.exemple` to have the list    
    - Then, run `python data/load_data_in_redis.py`

## **Run the app locally**

**1. Setup python environment:**

Run the following command to create a virtual environment and install all the requirements:
```bash
make env
make install_requirements
```

**2. Fill credentials in environment:**

You'll need to export the following variables in your environment. Check `credentials/env.sh.exemple` to have the list of variables to fill:
```bash
export REDIS_HOST="redis_host_url"
export REDIS_PORT="1234"
export REDIS_DB="your-redis-database-name"
export REDIS_PASSWORD="redis-db-password"
```

**3. Run the app locally:**
To run the app in your local environment, just run the following command:
```bash
make run_app
```

It will open a Streamlit window on your web-browser.

## **Run the app on a Saturn Cloud Deployment instance**

You can easily create a deployment instance to run your app in Saturn Cloud by copying the recipe stored in the file `saturn-deployment-recipe.json` at the root of the project. Here are the instructions to create your own instance:

1. First, you'll need to parametrize your credentials in Saturn Cloud so your instance can access them. Go to "Secrets" > "New", and create a secret for the 4 credentials variables you exported earlier.

2. Then, go to "Resources" > "New Deployment" > "Use a Recipe", and paste the content of `saturn-deployment-recipe.json` in the open window. A deployment instance will be created with app parameters.

3. Finally, you'll need to add the credentials that are necessary to run your app. After creating the instance, select it in "Resources", then go to "Secrets" > "Attach Secret Environment Variable", and select in the dropdown menu the secrets you defined in step 1. Be sure to assign the corresponding environment variable names to them.

4. Now you're ready to go! Click on "Overview" > "Start", and once the app is running, you can access it by clicking on the provided public URL.

Notes: 
- The deployment instance will directly pull the main branch of this repo to run the app with, but you can modify the branch it pulls by modifying it in "Git Repos" section. 
- You may need to link a Saturn SSH key the first time you run the app, the instructions to do so will then be displayed on Saturn directly. You will just have to add Saturn SSH Key to your GitHub profile.

## **About the Question Answering pipeline**

The goal of this app is to ease information retrieval on research papers by allowing users to ask questions to the app in a natural language and get answers from papers. To do that, we found this [kaggle article](https://www.kaggle.com/code/officialshivanandroy/question-answering-with-arxiv-papers-at-scale) that we got inspired from.

Basically when the user asks a question to the app, here is the following process in backend:
- 1. It queries the Redis Vector Search database.
- 2. Redis Vector Search DB returns the abstracts that are the closest in terms of vector similarity.
- 3. Then, it leverages a question answering (QA) algorithm to extract the answers to the user query.

We relied on the [haystack](https://haystack.deepset.ai/) framework to do QA at scale. For the sake of our usage there are 3 `haystack` components to understand:

* **Document Store**: Database storing the documents for our search. There are a lot of options already provided by `haystack` such as Elasticsearch, Faiss, OpenSearch, In-Memory, SQL ... We decided to create the `RedisDocumentStore` class to be able to benefit from the `haystack` framework while using the `Redis` database.
* **Retriever**: Fast, simple algorithm that identifies candidate passages from a large collection of documents. Algorithms include TF-IDF or BM25, EmbeddingRetriever... We chose an `EmbeddingRetriever` with the same embedding model that was used to feed the `Redis` database.
* **Reader**: the reader takes multiple texts as input and returns top-n answers with corresponding confidence scores. You can just load a pretrained model from Hugging Face's model hub or fine-tune it to your own domain data. We used the suggested model `sentence-transformers/all-mpnet-base-v2` as it is the state of the art model provided in the [haystack benchmark](https://haystack.deepset.ai/benchmarks) and that the first results looked pretty good for a first baseline. If we had more time we would have benched other models and tried a fine tuned model to our own dataset.

## **Next steps**

The app was designed in a limited amount of time, and there are obviously many improvements to be made, and features to explore. 

Here is a non-exhaustive snapshot of some ideas we have:

### Improving current features
- We used a generic embedding model to embed the abstracts. It may be relevant to try fine-tuned models on arXiv data to see if it improves  similarity search performances
- Same for QA model, trying other models may improve question answering performances
- We currently retrieve 10 documents when the app run on CPU, and 100 if the app run on GPU. It can be a relativelly low number of text to answer difficult questions. It may be interesting to have an adaptative number of retrieved documents depending on the quantity of answers found for a particular question

### Adding new features
- Integrating the redis database uploading process in the  `RedisDocumentStore` as it is done by `haystack` for [other document stores objects](https://github.com/deepset-ai/haystack/tree/main/haystack/document_stores)
- Adding a generative QA pipeline to give a single answer to the question at the beginning and keep the extractive one to illustrate the answer with examples
- Adding a time series representation of the papers on which the answer is found to give a visual timeline of those papers
- Splitting the deployment of the front streamlit app and the back ML pipeline > Host the app on a basic CPU instance and deploy the ML pipeline as an endpoint on a GPU instance to respect the single responsibility principle and better manage costs.

## Interested in contributing?
This is a new project. Comment on an open issue or create a new one. We can triage it from there.

## Additional links
- [ArXiv Kaggle Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)
- [Hackathon Page](https://hackathon.redisventures.com/)
- [MLOps Community Slack channel](https://join.slack.com/t/mlops-community/shared_invite/zt-1cjmjku5d-ZhJitSlS0VtqfCcwRpn_CQ)
- [Redis](https://redis.io/)
- [Saturn Cloud](https://saturncloud.io/)
- [Kaggle Question & Answering with ArXiV papers at scale](https://www.kaggle.com/code/officialshivanandroy/question-answering-with-arxiv-papers-at-scale)
- [haystack](https://haystack.deepset.ai/)
