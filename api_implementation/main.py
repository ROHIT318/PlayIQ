from fastapi import FastAPI, HTTPException
from typing import Dict
import numpy as np

app = FastAPI()

@app.get('/call_chat_model/{input_prompt}')
def call_chat_model(input_prompt: str) -> str:
    print(input_prompt)
    res = [
        "This is answer to q1.",
        "This is answer to q2.",
        "This is answer to q3.",
        "This is answer to q4."
    ]
    try:
        res_index = np.random.randint(0,len(res))
        return res[res_index]
    except:
        raise HTTPException(status_code=404, detail="Some Error Happened....")