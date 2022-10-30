import time

import numpy as np
import streamlit as st
from redis.commands.search.query import Query

from config.redis_config import INDEX_NAME, SEARCH_TYPE
from redis_player_one.embedder import make_embeddings
from redis_player_one.redis_client import redis_client

st.sidebar.title('Redis Player One - Similarity Search Engine')


def create_query(
    categories: list,
    years: list,
    search_type: str = SEARCH_TYPE,
    number_of_results: int = 10
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
    base_query = f'{tag}=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]'
    return Query(base_query)\
        .sort_by("vector_score")\
        .paging(0, number_of_results)\
        .return_fields("paper_id", "vector_score", "year", "title", "abstract")\
        .dialect(2)


def submit_text(text: str, date_range: list, nb_articles: int):
    q = create_query(categories=None,
                     years=date_range,
                     search_type=SEARCH_TYPE,
                     number_of_results=nb_articles)

    # Vectorize the query
    query_vector = make_embeddings(text).astype(np.float32).tobytes()
    params_dict = {"vec_param": query_vector}

    # Execute the query
    results = redis_client.ft(INDEX_NAME).search(q, query_params=params_dict)
    return results


def plot_results(results):
    values_to_plot = []
    for i, paper in enumerate(results.docs):
        values_to_plot.append(
            {
                "year": paper.year,
                "similarity_score": 1 - float(paper.vector_score),
            }
        )
    st.line_chart(values_to_plot, x="year", y="similarity_score")


def app():
    user_text = st.sidebar.text_input(label="Enter some text here 👇", value="", max_chars=2000, key="user_text_input")
    nb_articles = st.sidebar.number_input("Insert the number of simillar articles to retrieve", step=1, min_value=0)
    date_range = st.sidebar.slider('Select a range of dates', 2015, 2022, (2016, 2019))
    clicked = st.sidebar.button('Submit')
    if clicked and user_text and nb_articles > 0:
        st.write("You entered: ", user_text)
        with st.spinner("Computing similarity research"):
            start_time = time.time()
            results = submit_text(
                text=user_text,
                date_range=list(map(str, list((range(*date_range))))),
                nb_articles=nb_articles
            )
            end_time = time.time()
        st.sidebar.success(f"Found {nb_articles} abstracts in {round(end_time - start_time, 2)} seconds!")
        if results:
            for i, paper in enumerate(results.docs):
                paper_abstract = paper.abstract
                paper_title = paper.title
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f'<h2 style="color:#2892D7;font-size:24px;">Abstract #{i + 1} - {paper_title}</h1>',
                                unsafe_allow_html=True)
                    st.write(paper_abstract)
                with col2:
                    st.markdown('<h2 style="color:#ff0000;font-size:24px;">Similarity score</h1>',
                                unsafe_allow_html=True)
                    st.write(f"{round(100*(1 - float(paper.vector_score)), 1)}%")
                    st.markdown('<h2 style="color:#ff0000;font-size:24px;">Link to the article</h1>',
                                unsafe_allow_html=True)
                    st.write(f"https://arxiv.org/abs/{paper.id}")
                st.markdown("""---""")


if __name__ == "__main__":
    app()
