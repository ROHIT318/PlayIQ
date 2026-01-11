import streamlit as st
# Once langchain and fastapi are implemented, remove this
import numpy as np
import time
import os
import datetime
from dotenv import load_dotenv
import boto3
import requests
import json

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
USER_AVATAR = os.getenv('USER_AVATAR')
ASSISTANT_AVATAR = os.getenv('ASSISTANT_AVATAR')


chat_media_path = os.path.join(os.getcwd(), "webpage", "utility")
if os.path.exists(chat_media_path) == False:
    os.mkdir(chat_media_path)
    os.mkdir(os.path.join(os.getcwd(), "webpage", "utility", "chat_media"))
    os.mkdir(os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "images"))
    os.mkdir(os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "videos"))

img_media_path = os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "images")
vid_media_path = os.path.join(os.getcwd(), "webpage", "utility", "chat_media", "videos")

s3 = boto3.client('s3', aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    region_name=os.getenv("REGION_NAME"))
BUCKET_NAME = os.getenv('s3_bucket')

def get_presigned_url(s3_key_file_path, expires=3600):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": s3_key_file_path},
        ExpiresIn=expires,
    )


st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-row {
    display: flex;
    align-items: flex-end;
    width: 100%;
    gap: 8px;
}

.chat-row.user {
    justify-content: flex-end;
}

.chat-row.assistant {
    justify-content: flex-start;
}
            
.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
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
    st.session_state.messages = [{'role': 'assistant', 'content': 'Hello, How can I help you?', 'media_file_path': []}]

if "username" not in st.session_state:
    st.session_state.username = np.random.randint(100000, 999999)

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

    # with st.chat_message('assistant'):
    #     st.write("Hello, How can I help you?")

    total_msgs = len(st.session_state.messages)
    i=0

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # -- fix this
    st.session_state.username = '1'
    fetch_msg_payload = {'user_id': st.session_state.username, 'chat_name': 'test'}
    messages = requests.post(f'{BASE_URL}/get_chat/', json=fetch_msg_payload).content.decode('utf-8')
    messages = json.loads(messages)
    print(messages)
    for msg in messages:
        role = msg["role"]
        content = msg["chat_msg"]
        media_files = msg.get("media_file_path", [])

        bubble_html = ""

        # 1️⃣ MEDIA FIRST (on top)
        for media in media_files:
            media_url = get_presigned_url(media)
            print(media_url)

            if any(ext in media.lower() for ext in [".jpg", ".jpeg", ".png"]):
                bubble_html += f'<img src="{media_url}" style="width:80%; border-radius:12px; margin-bottom:6px;" />'                    

            elif ".mp4" in media.lower():
                bubble_html += f'<video width="200" controls><source src="{media_url}" type="video/mp4"></video>'

        # 2️⃣ TEXT CAPTION (below media)
        if content:
            bubble_html += f"<div>{content}</div>"

        avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR

        if role == "assistant":
            html = f"""
            <div class="chat-row assistant">
                <img class="avatar" src="{avatar}" />
                <div class="chat-bubble assistant">
                    {bubble_html}
                </div>
            </div>
            """
        else:
            html = f"""
            <div class="chat-row user">
                <div class="chat-bubble user">
                    {bubble_html}
                </div>
                <img class="avatar" src="{avatar}" />
            </div>
            """

        st.markdown(html, unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True)


    if user_msg := st.chat_input("What is up?", accept_file='multiple', file_type=['jpg', 'png', 'jpeg', 'mp4'], ):
        asst_msg = call_chat_model(user_msg.text)
        # asst_msg = requests.get(f'{BASE_URL}/call_chat_model/{user_msg.text}').content.decode('utf-8')


        media_file_path = [] 
        for file in user_msg["files"]:            
            if file.name.lower().endswith(('.mp4')):
                file_name = str(st.session_state.username) + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.mp4'
                vid_s3_path = "chat_media/videos/" + file_name
                s3.upload_fileobj(
                    file, 
                    BUCKET_NAME, 
                    vid_s3_path, 
                    ExtraArgs={"ContentType": file.type}
                )
                media_file_path.append(vid_s3_path)
            
            elif  file.name.lower().endswith(('jpg', 'jpeg', 'png')):
                file_name = str(st.session_state.username) + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.jpg'
                img_s3_path = "chat_media/images/" + file_name
                s3.upload_fileobj(
                    file, 
                    BUCKET_NAME, 
                    img_s3_path, 
                    ExtraArgs={"ContentType": file.type}
                )
                media_file_path.append(img_s3_path)
        
        # For testing purpose. DO NOT DELETE.
        # st.session_state.messages.append({'role': 'user', 'content': user_msg.text, 'media_file_path': media_file_path})
        # st.session_state.messages.append({'role': 'assistant', 'content': asst_msg, 'media_file_path': []})

        # -- fix this role
        payload = {'user_id': st.session_state.username, 'role': 'user', 'chat_name': 'test', 'chat_msg': user_msg.text, 'chat_media': media_file_path}
        requests.post(f'{BASE_URL}/save_chat/', data=payload)
        # -- fix this role
        payload = {'user_id': st.session_state.username, 'role': 'assistant', 'chat_name': 'test', 'chat_msg': asst_msg, 'chat_media': media_file_path}
        requests.post(f'{BASE_URL}/save_chat/', data=payload)

        # time.sleep(5)
        st.rerun()
