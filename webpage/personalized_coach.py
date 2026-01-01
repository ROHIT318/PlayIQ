import streamlit as st
from typing import Str, Dict
# Once langchain and fastapi are implemented, remove this
import random

if "messages" not in st.session_state:
    st.session_state.messagess = Dict()

def call_chat_model(msg: Str) -> Str:
    res = [
        "This is answer to q1",
        "This is answer to q2",
        "This is answer to q3",
        "This is answer to q4"
    ]
    res_index = random.random.int()
    return res[res_index]

with st.container(border=True):

    with st.chat_message('assistant'):
        st.write("Hello, How can I help you?")
    
    with st.chat_message('user'):
        st.write("Here is question 1?")

    user_msg = st.chat_input("What is up?")
    st.session_state.messages.add('user', user_msg)
    assistant_msg = call_chat_model(user_msg)
    st.session_state.messages.add('assistant', assistant_msg)
