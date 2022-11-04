import time

import streamlit as st
from lib.app_utils import button_callback, display_categories, display_user_inputs, instanciate_button, load_fontawesome
from lib.query_utils import instanciate_retriever, make_qa_query

from config import ASKYVES_IMG_PATH, REDIS_ICON_PATH


def app():
    st.set_page_config(page_title="Redis Player One", page_icon=REDIS_ICON_PATH, layout="wide")
    load_fontawesome()
    pipe = instanciate_retriever()
    instanciate_button("button1")
    st.sidebar.image(ASKYVES_IMG_PATH)
    with st.form(key="content_section"):
        with st.sidebar:
            user_question, date_range = display_user_inputs()
            st.form_submit_button("Submit to Yves", on_click=button_callback, kwargs={"name": "button1"})

    if st.session_state["button1"]:
        if not user_question:
            st.error("please type a question in the searchbar")
        else:
            st.markdown(
                f'<h1 style="color:#000000;font-size:34px;">You\'ve asked: <br><em style="color:#FFFFFF;font-size:30px;">&laquo; {user_question} &raquo;</em></h1>',
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

            if len(results["answers"]) > 0:
                st.sidebar.success(
                    f"Top {len(results['answers'])} answers found in {round(end_time - start_time, 2)} seconds!"
                )
            else:
                st.sidebar.error("Yves couldn't find an answer to your question...")

            if results:
                answers = sorted(results["answers"], key=lambda x: x.score, reverse=True)
                for i, paper in enumerate(answers):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(
                            f'<h1> <a style="color:#F71734;font-size:22px;" href="https://arxiv.org/abs/{paper.document_id}"> Abstract #{i + 1} - {paper.meta["name"]}</h1>',
                            unsafe_allow_html=True,
                        )
                        abstact_str = paper.context
                        start, end = paper.offsets_in_document[0].start, paper.offsets_in_document[0].end
                        abstact_str = f'{abstact_str[:start]}<b style="background-color:#FFBA08;color:#4C4C4C;">{abstact_str[start:end]}</b>{abstact_str[end:]}'
                        st.markdown(f'<p style="color:#FFF;font-size:19px;">{abstact_str}</p>', unsafe_allow_html=True)

                    with col2:
                        st.markdown(
                            '<h1 style="font-size:25px;"> </h1>',
                            unsafe_allow_html=True,
                        )
                        similarity_score_str = f"{round(100 *float(paper.score), 1)}%"
                        crosshairs_icon = '<i class="fa-solid fa-crosshairs" style="color:#F71734;font-size:19px;"></i>'
                        st.markdown(
                            f'<h2 style="color:#FFFFFF;font-size:19px;"> {crosshairs_icon} &nbsp {similarity_score_str}</h2>',
                            unsafe_allow_html=True,
                        )

                        if paper.meta["update_date"]:
                            calendar_icon = (
                                '<i class="fa-regular fa-calendar" style="color:#F71734;font-size:19px;"></i>'
                            )
                            st.markdown(
                                f'<h1 style="color:#FFFFFF;font-size:19px;"> {calendar_icon} &nbsp {paper.meta["update_date"]}</h1>',
                                unsafe_allow_html=True,
                            )

                        if paper.meta["categories"]:
                            def_str = display_categories(paper)
                        else:
                            def_str = "Unknown categories"
                        st.markdown(
                            f'<h1 style="color:#FFFFFF;font-size:14px;"> {def_str}</h1>', unsafe_allow_html=True
                        )
                    st.markdown("""---""")


if __name__ == "__main__":
    app()
