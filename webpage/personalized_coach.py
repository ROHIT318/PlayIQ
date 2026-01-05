import streamlit as st
from typing import Dict
# Once langchain and fastapi are implemented, remove this
import numpy as np
import time
import os
import datetime
import requests
from dotenv import load_dotenv
import base64
import streamlit.components.v1 as components

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

chat_media_path = os.path.join(os.getcwd(), "webpage", "utility")
if os.path.exists(chat_media_path) == False:
    os.mkdir(chat_media_path)
    os.mkdir(os.path.join(os.getcwd(), "webpage", "utility", "chat_media"))
    os.mkdir(os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "images"))
    os.mkdir(os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "videos"))


st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-row {
    display: flex;
    width: 100%;
}

.chat-row.user {
    justify-content: flex-end;
}

.chat-row.assistant {
    justify-content: flex-start;
}

.chat-bubble {
    max-width: 70%;
    padding: 10px 14px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.4;
    word-wrap: break-word;
}

.chat-bubble.user {
    background-color: #1f6feb;
    color: white;
    border-bottom-right-radius: 4px;
}

.chat-bubble.assistant {
    background-color: #f1f3f5;
    color: #111;
    border-bottom-left-radius: 4px;
}

.file-card {
    margin-top: 8px;
    padding: 8px 10px;
    background: #fff;
    border-radius: 10px;
    border: 1px solid #ddd;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


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
    # for i, msg in enumerate(st.session_state.messages):
    #     if i==total_msgs and msg['role']=='assistant':
    #         with st.chat_message(msg['role']):
    #             st.write_stream(get_stream_obj(msg['content']), cursor='||')
    #     else:
    #         with st.chat_message(msg['role']):
    #             st.write(msg['content'])
    #             if msg['role']!='assistant' and len(msg['media_file_path']) != 0:
    #                 for media_file_path in msg['media_file_path']:
    #                     if media_file_path.lower().endswith('.mp4'):
    #                         st.video(media_file_path, width=200)
    #                     elif media_file_path.lower().endswith(('.jpg', '.jpeg', 'png')):
    #                         st.image(media_file_path, width=200)
    #     i+=1
    #             # time.sleep(5)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        media_files = msg.get("media_file_path", [])

        bubble_html = ""

        # 1️⃣ MEDIA FIRST (on top)
        # for media in media_files:
        #     filename = os.path.basename(media)

        #     if media.lower().endswith((".jpg", ".jpeg", ".png")):
        #         bubble_html += f"""
        #         <img src="data:image/png;base64,{base64.b64encode(open(media, "rb").read()).decode()}"
        #             style="width:100%; border-radius:12px; margin-bottom:6px;" />
        #         """

        #     elif media.lower().endswith(".mp4"):
        #         bubble_html += f"""
        #             <video controls style="width:100%; border-radius:12px;">
        #                 <source src="{media}" type="video/mp4">
        #             </video>
        #         """

        #     elif media.lower().endswith(".pdf"):
        #         bubble_html += f"""
        #         <div class="file-card">📄 {filename}</div>
        #         """

        # 2️⃣ TEXT CAPTION (below media)
        if content:
            bubble_html += f"<div>{content}</div>"

        st.markdown(
            f"""
            <div class="chat-row {role}">
                <div class="chat-bubble {role}">
                    <img src="{media_files[0]}"/>
                    # {bubble_html}
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


    if user_msg := st.chat_input("What is up?", accept_file='multiple', file_type=['jpg', 'png', 'jpeg', 'mp4'], ):
        asst_msg = call_chat_model(user_msg.text)
        # asst_msg = requests.get(f'{BASE_URL}/call_chat_model/{user_msg.text}').content.decode('utf-8')


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
        st.session_state.messages.append({'role': 'assistant', 'content': asst_msg, 'media_file_path': []})

        # time.sleep(5)
        st.rerun()
