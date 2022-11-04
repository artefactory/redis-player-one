import time

import streamlit as st
from lib.app_utils import button_callback, instanciate_button
from lib.query_utils import instanciate_retriever, make_qa_query

from config.redis_config import ROOT_PATH
from data.categories import CAT_TO_DEFINITION_MAP


def app():
    st.set_page_config(page_title="Redis Player One", page_icon="https://arxiv.org/favicon.ico", layout="wide")
    pipe = instanciate_retriever()
    instanciate_button("button1")
    st.sidebar.image(str(ROOT_PATH / "data/askiv.png"))
    with st.form(key="content_section"):
        with st.sidebar:
            user_question, date_range = _display_user_inputs()
            st.form_submit_button("Submit to Yves", on_click=button_callback, kwargs={"name": "button1"})

    if st.session_state["button1"]:
        if not user_question:
            st.error("please type a question in the searchbar")
        else:
            st.markdown(
                f'<h2 style="color:#FFFFFF;font-size:30px;">You\'ve asked: <br><em>"{user_question}"</em></h1>',
                unsafe_allow_html=True,
            )
            st.markdown("""---""")

            with st.spinner("Asking Yves for answers..."):
                start_time = time.time()
                results = make_qa_query(
                    pipe=pipe,
                    text=user_question,
                    date_range=list(map(str, list((range(date_range[0], date_range[1] + 1))))),
                )
                end_time = time.time()

            st.sidebar.success(
                f"Top {len(results['answers'])} answers found in {round(end_time - start_time, 2)} seconds!"
            )

            if results:
                answers = sorted(results["answers"], key=lambda x: x.score, reverse=True)
                for i, paper in enumerate(answers):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(
                            f'<h2 style="color:#2892D7;font-size:19px;">Abstract #{i + 1} - {paper.meta["name"]}</h1>',
                            unsafe_allow_html=True,
                        )
                        abstact_str = paper.context
                        start, end = paper.offsets_in_document[0].start, paper.offsets_in_document[0].end
                        abstact_str = f'{abstact_str[:start]}<b style="background-color:#FFBA08;color:#4C4C4C;">{abstact_str[start:end]}</b>{abstact_str[end:]}'
                        st.markdown(f'<p style="color:#FFF;font-size:19px;">{abstact_str}</p>', unsafe_allow_html=True)

                    with col2:
                        similarity_score_str = f"{round(100 *float(paper.score), 1)}%"
                        st.markdown(
                            '<h2 style="color:#F71734;font-size:19px;">Relevance score:</h2>', unsafe_allow_html=True
                        )
                        st.markdown(
                            f'<h2 style="color:#FFFFFF;font-size:19px;">📊 {similarity_score_str}</h2>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<h1 style="color:#F71734;font-size:16px;">🔗 <a href="https://arxiv.org/abs/{paper.document_id}">Link to the article</a></h1>',
                            unsafe_allow_html=True,
                        )

                        if paper.meta["update_date"]:
                            st.markdown(
                                '<h1 style="color:#F71734;font-size:14px;"><u>Updated on:</u></h1>',
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f'<h1 style="color:#FFFFF;font-size:14px;">📆 {paper.meta["update_date"]}</h1>',
                                unsafe_allow_html=True,
                            )

                        if paper.meta["categories"]:
                            def_str = _display_categories(paper)
                        else:
                            def_str = "Unknown categories"
                        st.markdown(
                            '<h1 style="color:#F71734;font-size:14px;"><u>Categories:</u></h1>', unsafe_allow_html=True
                        )
                        st.markdown(f'<h1 style="color:#FFFFFF;font-size:14px;">{def_str}</h1>', unsafe_allow_html=True)
                    st.markdown("""---""")


def _display_categories(paper):
    cats_list = paper.meta["categories"].split(",")
    def_list = sorted(set(map(lambda x: CAT_TO_DEFINITION_MAP.get(x, x), cats_list)))
    def_list[0] = f"✅ {def_list[0]}"
    def_str = "<br>✅ ".join(def_list)
    return def_str


def _display_user_inputs():
    user_question = st.text_input(label="Enter your question here 👇", max_chars=2000, key="user_question_input")
    date_range = st.slider("Select a range of dates", 2008, 2022, (2008, 2022))
    return user_question, date_range


if __name__ == "__main__":
    app()
