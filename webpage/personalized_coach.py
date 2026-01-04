import streamlit as st
from typing import Dict
# Once langchain and fastapi are implemented, remove this
import numpy as np
import time
import os
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

chat_media_path = os.path.join(os.getcwd(), "webpage", "utility", "chat_media")
if os.path.exists(chat_media_path) == False:
    os.mkdir(chat_media_path)

img_media_path = os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "images")
if os.path.exists(img_media_path) == False:
    os.mkdir(img_media_path)

vid_media_path = os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "videos")
if os.path.exists(vid_media_path) == False:
    os.mkdir(vid_media_path)

if "messages" not in st.session_state:
    st.session_state.messages = []

def call_chat_model(msg: str) -> str:
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
    for i, msg in enumerate(st.session_state.messages):
        if i==total_msgs-1 and msg['role']=='assistant':
            with st.chat_message(msg['role']):
                st.write_stream(get_stream_obj(msg['content']), cursor='||')
        else:
            with st.chat_message(msg['role']):
                st.write(msg['content'])
                if msg['role']!='assistant' and len(msg['media_file_path']) != 0:
                    for media_file_path in msg['media_file_path']:
                        if media_file_path.lower().endswith('.mp4'):
                            st.video(media_file_path, width=200)
                        elif media_file_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                            st.image(media_file_path, width=200)
        i+=1
                # time.sleep(5)

    if user_msg := st.chat_input("What is up?", accept_file='multiple', file_type=['jpg', 'png', 'jpeg', 'mp4'], ):
        # asst_msg = call_chat_model(user_msg.text)
        asst_msg = requests.get(f'{BASE_URL}/call_chat_model/{user_msg.text}').content.decode('utf-8')

        media_file_path = [] 
        for file in user_msg["files"]:
            username = np.random.randint(100000, 999999)
            
            if file.name.lower().endswith(('.mp4')):
                vid_save_filepath = os.path.join(vid_media_path, str(username) + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.mp4')
                with open(vid_save_filepath, 'wb') as f:
                    file.seek(0)
                    f.write(file.read())
                f.close()
                media_file_path.append(vid_save_filepath)
            
            elif  file.name.lower().endswith(('jpg', 'jpeg', 'png')):
                img_save_filepath = os.path.join(img_media_path, str(username) + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.jpg')
                with open(img_save_filepath, 'wb') as f:
                    file.seek(0)
                    f.write(file.read())
                f.close()
                media_file_path.append(img_save_filepath)
        
        st.session_state.messages.append({'role': 'user', 'content': user_msg.text, 'media_file_path': media_file_path})
        st.session_state.messages.append({'role': 'assistant', 'content': asst_msg, 'media_file_path': None})

        # time.sleep(5)
        st.rerun()
