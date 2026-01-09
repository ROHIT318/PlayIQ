from fastapi import FastAPI, HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage
from api_implementation.db_details.schemas import ChatDetailsModel, UserAccountModel
from api_implementation.db_details.db_connection import ChatDetails, UserAccount, engine

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')
# repo_id = os.getenv('repo_id')

app = FastAPI()

# Create table in database
UserAccount.metadata.create_all(bind=engine)
ChatDetails.metadata.create_all(bind=engine)

@app.post('/save_chat/')
def save_chat(chat_details: ChatDetailsModel):
    pass

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