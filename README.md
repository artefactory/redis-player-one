
<div align="center">
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><img src="data/askiv.png" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://docsearch.redisventures.com"><b>Hosted Demo</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

# Ask' Yves

Yves Saint Laurent was one of the greatest minds of french history. He spent a lot of time reading scientific papers on arXiv.

Ask him anything. He will have an answer. Probably not the right one, but you might be surprised 😅

## How it works
# TODO

## Getting Started

### Run

`make run_app`

### Set-up

The steps below outline how to get this app up and running on your machine.

`make env`
`make install_requirements`
Create a `.env` file in `./credentials`


## Download arXiv Dataset

Pull the arXiv dataset from the the following [Kaggle link](https://www.kaggle.com/Cornell-University/arxiv).

Download and extract the zip file and place the resulting json file (`arxiv-metadata-oai-snapshot.json`) in the `data/` directory.

## Embedding Creation

**1. Setup python environment:**
- If you use conda, take advantage of the Makefile included here: `make env`
- Otherwise, setup your virtual env however you wish and install python deps in `requirements.txt`

**2. Use the notebook:**
- Run through the [`arxiv-embeddings.ipynb`](data/arxiv-embeddings.ipynb) notebook to generate some sample embeddings.


## Application

This app was built as a Single Page Application (SPA) with the following components:

- **[Redis Stack](https://redis.io/docs/stack/)**: Vector database + JSON storage
- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.8)
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** for schema and validation
- **[React](https://reactjs.org/)** (with Typescript)
- **[Redis OM](https://redis.io/docs/stack/get-started/tutorials/stack-python/)** for ORM
- **[Docker Compose](https://docs.docker.com/compose/)** for development
- **[MaterialUI](https://material-ui.com/)** for some UI elements/components
- **[React-Bootstrap](https://react-bootstrap.github.io/)** for some UI elements
- **[Huggingface Tokenizers + Models](https://huggingface.co/sentence-transformers)** for vector embedding creation

Some inspiration was taken from this [Cookiecutter project](https://github.com/Buuntu/fastapi-react)
and turned into a SPA application instead of a separate front-end server approach.

### Launch

**To launch app, run the following:**
- `docker compose up` from the same directory as `docker-compose.yml`
- Navigate to `http://localhost:8888` in a browser

**Building the containers manually:**

The first time you run `docker compose up` it will automatically build your Docker images based on the `Dockerfile`. However, in future passes when you need to rebuild, simply run: `docker compose up --build` to force a new build.

### Using a React dev env
It's typically easier to manipulate front end code in an interactive environment (**outside of Docker**) where one can test out code changes in real time. In order to use this approach:

1. Follow steps from previous section with Docker Compose to deploy the backend API.
2. `cd gui/` directory and use `yarn` to install packages: `yarn install --no-optional` (you may need to use `npm` to install `yarn`).
3. Use `yarn` to serve the application from your machine: `yarn start`.
4. Navigate to `http://localhost:3000` in a browser.
5. Make front end changes in realtime.

### Troubleshooting

- Issues with Docker? Run `docker system prune`, restart Docker Desktop, and try again.
- Open an issue here on GitHub and we will be as responsive as we can!


### Interested in contributing?
This is a new project. Comment on an open issue or create a new one. We can triage it from there.


### Next steps
# TODO