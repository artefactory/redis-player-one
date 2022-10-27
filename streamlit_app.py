import streamlit as st

st.title('Redis Player One - Search Engine')

st.subheader('Type a topic to find related articles...')
selected = st.text_input("", "")
if selected:
    st.write(f"Example of article of selected topic: {selected}")