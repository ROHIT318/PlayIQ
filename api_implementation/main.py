from fastapi import FastAPI, HTTPException, Depends
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage
from api_implementation.db_details.schemas import ChatDetailsModel, UserAccountModel, GetChatModel, SaveChatModel
from api_implementation.db_details.db_connection import ChatDetails, UserAccount, engine, SessionCreator
from datetime import datetime
from sqlalchemy.orm import Session

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')
# repo_id = os.getenv('repo_id')

app = FastAPI()

# Create table in database
UserAccount.metadata.create_all(bind=engine)
ChatDetails.metadata.create_all(bind=engine)

# Generator for db connection
def db_conn():
    try:
        db = SessionCreator()
        yield db
        db.commit()
    finally:
        db.close()

# Save chat details in relational database
@app.post('/save_chat/')
def save_chat(chat_details: SaveChatModel, db_conn: Session = Depends(db_conn)):
    # print(chat_details)
    try:
        # print(chat_details.chat_media)
        db_conn.add(ChatDetails(user_id=chat_details.user_id, role=chat_details.role, chat_name=chat_details.chat_name, chat_msg=chat_details.chat_msg, media_file_path=chat_details.chat_media))
    except:
        raise HTTPException(status_code=404, detail="Some Error Happened !!")

# Get specific chat details from relational database
@app.post('/get_chat/')
def get_chat(get_chat_model: GetChatModel, db_conn: Session = Depends(db_conn)):
    # print(chat_details)
    # try:
    chat_msgs = db_conn.query(ChatDetails).filter(ChatDetails.user_id==get_chat_model.user_id, ChatDetails.chat_name==get_chat_model.chat_name).all()
    if len(chat_msgs)==0:
        return {'details': 'No messages'}
    else:
        return chat_msgs
    # except:
    #     raise HTTPException(status_code=404, detail="Some Error Happened !!")
    
# Get all chat details from relational database
@app.post('/get_all_chat/')
def get_all_chat(db_conn: Session = Depends(db_conn)):
    # print(chat_details)
    try:
        chat_msgs_obj = db_conn.query(ChatDetails).all()
        if chat_msgs_obj is None:
            return {'details': 'No messages'}
        else:
            return chat_msgs_obj
    except:
        raise HTTPException(status_code=404, detail="Some Error Happened !!")
    
# Get chat details from relational database
@app.delete('/delete_chat/')
def delete_chat(chat_id: str, user_id: str, chat_name: str, db_conn: Session = Depends(db_conn)):
    try:
        chat_msg = db_conn.query(ChatDetails).filter(ChatDetails.chat_id==chat_id, ChatDetails.user_id==user_id, ChatDetails.chat_name==chat_name).first()
        # print(chat_msg)
        if chat_msg is None:
            return {'details': 'No messages'}
        else:
            db_conn.delete(chat_msg)
    except:
        raise HTTPException(status_code=404, detail="Some Error Happened !!")

# Update existing messages(only text, not media details) in chat message
@app.put('/update_chat/')
def update_chat(chat_id: str, user_id: str, updated_chat_msg: str, db_conn: Session = Depends(db_conn)):
    try:
        chat_msg_obj = db_conn.query(ChatDetails).filter(ChatDetails.chat_id==chat_id, ChatDetails.user_id==user_id)
        if chat_msg_obj is not None:
            chat_msg_obj.update({
                ChatDetails.chat_msg: updated_chat_msg
            })
        else:
            return {'details': 'No message exists !!'}
    except:
        raise HTTPException(status_code=404, detail="Some Error Happened !!")

@app.post('/save_user/')
def save_user(user_account: UserAccountModel):
    pass


@app.get('/call_gemini_chat_model/{input_prompt}')
def call_gemini_chat_model(input_prompt: str) -> str:
    print(input_prompt)
    try:
        model = ChatGoogleGenerativeAI(
            # model="gemini-2.5-flash-tts", # Multimodal.
            model="gemini-2.5-flash-lite",
            # model="gemini-2.5-flash",
            # model="gemini-3-flash", # This didn't worked.
            # model="gemini-robotics-er-1.5-preview",

            # None are working for below
            # model="gemma-3-12b",
            # model="gemma-3-1b",
            # model="gemma-3-27b",
            # model="gemma-3-2b", 
            # model="gemma-3-4b",

            temperature=0.4,
            max_retries=1
        )

        messages = [("user", input_prompt)]
        assistant_msg = model.invoke(messages)
        print(assistant_msg.text)
        return assistant_msg.text
    except:
        raise HTTPException(status_code=404, detail="Some Error Happened....")
    

@app.get('/call_hugging_face_chat_model/{input_prompt}')
def call_hugging_face_model(input_prompt: str):
    hf_llm = HuggingFaceEndpoint(
        # repo_id="deepseek-ai/DeepSeek-R1-0528",
        repo_id="google/gemma-3-4b-it",
        max_length=50,
        temperature=0.4,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        provider="auto", 
    )

    chat = ChatHuggingFace(llm=hf_llm) 

    response = chat.invoke([
        HumanMessage(content=input_prompt)
    ])

    return {"response": response.content}


# 1. Save or sign-up user
@app.post("/signup/")
def user_signup():
    


# 2. Login user