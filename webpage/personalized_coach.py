import streamlit as st
from typing import Dict
# Once langchain and fastapi are implemented, remove this
import numpy as np
import time

if "messages" not in st.session_state:
    st.session_state.messages = []

def call_chat_model(msg: str) -> Str:
    res = [
        "This is answer to q1",
        "This is answer to q2",
        "This is answer to q3",
        "This is answer to q4"
    ]
    res_index = np.random.randint(0,len(res))
    return res[res_index]

st.title("Your Personalized Coach")
with st.container(border=True):

    with st.chat_message('assistant'):
        st.write("Hello, How can I help you?")

    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
            # time.sleep(5)

    if user_msg := st.chat_input("What is up?"):
        asst_msg = call_chat_model(user_msg)
        st.session_state.messages.append({'role': 'user', 'content': user_msg})
        st.session_state.messages.append({'role': 'assistant', 'content': asst_msg})
        # time.sleep(5)
        st.rerun()
