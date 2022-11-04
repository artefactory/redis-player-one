import streamlit as st

from assets.categories import CAT_TO_DEFINITION_MAP
from config import FONT_AWESOME_IMPORT


def load_fontawesome():
    st.markdown(FONT_AWESOME_IMPORT, unsafe_allow_html=True)


def button_callback(name: str) -> None:
    """Callback to change the session_state of the button to True
    Args:
        name (str): button name
    """
    st.session_state[name] = True


def instanciate_button(button_name: str) -> None:
    if button_name not in st.session_state:
        st.session_state[button_name] = False


def display_categories(paper):
    cats_list = paper.meta["categories"].split(",")
    def_list = sorted(set(map(lambda x: CAT_TO_DEFINITION_MAP.get(x, x), cats_list)))
    square_check = '<i class="fa-regular fa-square-check" style="color:#F71734;font-size:17px;"></i>'
    def_list[0] = f"{square_check} &nbsp {def_list[0]}"
    def_str = f"<br> {square_check} &nbsp ".join(def_list)
    return def_str


def display_user_inputs():
    user_question = st.text_input(label="Enter your question here 👇", max_chars=2000, key="user_question_input")
    date_range = st.slider("Select a range of dates", 2008, 2022, (2008, 2022))
    return user_question, date_range
