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

def get_stream_obj(input: str):
    for ch in input:
        yield ch
        time.sleep(0.1)

st.title("Your Personalized Coach")
with st.container(border=True):

    with st.chat_message('assistant'):
        st.write("Hello, How can I help you?")

    total_msgs = len(st.session_state.messages)
    i=0
    for msg in st.session_state.messages:
        if i==total_msgs-1 and msg['role']=='assistant':
            with st.chat_message(msg['role']):
                st.write_stream(get_stream_obj(msg['content']), cursor='||')
        else:
            with st.chat_message(msg['role']):
                st.write(msg['content'])
            i+=1
                # time.sleep(5)

    if user_msg := st.chat_input("What is up?"):
        asst_msg = call_chat_model(user_msg)
        st.session_state.messages.append({'role': 'user', 'content': user_msg})
        st.session_state.messages.append({'role': 'assistant', 'content': asst_msg})
        # time.sleep(5)
        st.rerun()
