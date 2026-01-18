from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from api_implementation.db_details.schemas import UserModel, SignupUserModel
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


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
    },
    {
        'user_id': 'user@example.com',
        'mail': 'user@example.com',
        'password': '$argon2id$v=19$m=65536,t=3,p=4$x9YNHLwOeGTqtnO7PMYsgA$iDlCV26550qZCYbiHhOvZNJfzncFf4VCLpskAqKmP6I',
        'token': '$argon2id$v=19$m=65536,t=3,p=4$x9YNHLwOeGTqtnO7PMYsgA$iDlCV26550qZCYbiHhOvZNJfzncFf4VCLpskAqKmP6I'
    }
]

resource = {"data": "secured data"}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")
ph = PasswordHash.recommended()

@app.get('/fetch_resource')
def fetch_resource(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    return resource

def get_password_hash(password):
    return ph.hash(password)

def verify_password(password, hashed_password):
    return ph.verify(password, hashed_password)

def check_user(username, pswd):
    for user in user_db:
        if user['mail'] == username:
            # print(user['mail'], get_password_hash('string'))
            is_user = verify_password(pswd, user['password'])
            # print(f"is_user: {is_user}")
            if is_user:
                token = 'Verified'
                return token
    return False

@app.post('/token')
def login(user_creds: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # print(user_creds.username)
    # print(user_creds.password)
    if user_creds.username is None or user_creds.password is None:  
        raise HTTPException(status=404, detail='Creds not received....')
    
    print(user_creds.username, user_creds.password)
    token = check_user(user_creds.username, user_creds.password)
    print(token)
    if token:
        print(token)
        return {"access_token": token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=401, detail='Creds not correct....')
    
@app.get('/get_all_user')
def get_all_user():
    return user_db

@app.post('/signup_user')
def signup_user(signup_user: SignupUserModel):
    # print(signup_user)
    hashed_password = get_password_hash(signup_user.pswd)
    user_db.append({'user_id': signup_user.mail, 'mail': signup_user.mail, 'password': hashed_password, 'token': hashed_password})
    return {"detail": "Profile created successfuly...."}

@app.delete('/delete_user')
def delete_user():
    pass