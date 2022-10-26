import streamlit as st
import pandas as pd
import numpy as np

st.title('Redis Player One - Search Engine')

st.write(pd.DataFrame({"This is": ["A", "TEST"]}))

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write("HELLO")

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
st.write(hour_to_filter)

st.subheader('Text search bar test')
selected = st.text_input("", "Search...")