from fastapi import FastAPI, HTTPException
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

app = FastAPI()

@app.get('/call_chat_model/{input_prompt}')
def call_chat_model(input_prompt: str) -> str:
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