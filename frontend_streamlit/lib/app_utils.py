import streamlit as st


def button_callback(name: str) -> None:
    """Callback to change the session_state of the button to True
    Args:
        name (str): button name
    """
    st.session_state[name] = True


def instanciate_button(button_name: str) -> None:
    if button_name not in st.session_state:
        st.session_state[button_name] = False
