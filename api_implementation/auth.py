from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from api_implementation.db_details.schemas import UserModel
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv['SECRET_KEY']
ALGORITHM = os.getenv['ALGORITHM']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

user_db = [ {
        'user_id': 'rohit@playiq.com',
        'mail': 'rohit@playiq.com',
        'password': 'rohitpswd',
        'token': 'rohittoken'
    },
    {
        'user_id': 'sharma@playiq.com',
        'mail': 'sharma@playiq.com',
        'password': 'sharmapswd',
        'token': 'sharmatoken'
    }
]

resource = {"data": "secured data"}


@app.get('/fetch_resource')
def fetch_resource(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    return resource

password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)

def check_user(username, pswd):
    user_creds = {}
    hash_pswd = jwt.encode()
    for user in user_db:
        if user['mail'] == username and user['password'] == pswd:
            user_creds['sub'] = pswd
            user_creds.update({'': })
            token = jwt.encode(user_creds, SECRET_KEY, algorithm=ALGORITHM)
            return token
    return False

@app.post('/token/')
def login(user_creds: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # print(user_creds.username)
    # print(user_creds.password)
    if user_creds.username is None or user_creds.password is None:  
        raise HTTPException(status=404, detail='Creds not received....')
    
    token = check_user(user_creds.username, user_creds.password)
    if token:
        print(token)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail='Creds not correct....')