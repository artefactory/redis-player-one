import streamlit as st

from redis_player_one.redis_client import redis_client, retrieve_paper


st.title('Redis Player One - Search Engine')
# Add it in header ? With buttons to click on links
# - Path to the dataset for example

st.subheader('Type a topic to find related articles...')
nb_articles = st.number_input("Insert a number of articles to retrieve", step=1)


left_side, right_side = st.columns([1, 1])
# Button for filtering by date
date_list = [i for i in range(2022, 1985, -1)]
with left_side:
    st.selectbox("Filter by date", date_list)

# Button for filtering by category
with right_side:
    st.selectbox("Filter by category", ("a", "b", "c"))

# Button to launch request

if nb_articles:
    st.write(nb_articles)
    articles_keys = redis_client.keys()[:nb_articles]
    st.write(articles_keys)
    for key in articles_keys:
        paper = retrieve_paper(redis_client, key)
        st.write(paper)
