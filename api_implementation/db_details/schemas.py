from pydantic import BaseModel, EmailStr, SecretStr
from typing import List
from datetime import datetime

class ChatDetailsModel(BaseModel):
    chat_id: str
    user_id: str
    role: str
    chat_name: str
    chat_msg: str
    media_file_path: List[str]
    created_on: datetime

class UserAccountModel(BaseModel):
    user_id: str
    mail: EmailStr
    pswd: SecretStr
    is_active: bool
    created_on: datetime

class GetChatModel(BaseModel):
    user_id: str
    chat_name: str

class SaveChatModel(BaseModel):
    user_id: str
    role: str
    chat_name: str
    chat_msg: str
    chat_media: List[str]

# User authentication
class UserModel(BaseModel):
    user_id: str
    mail: EmailStr
    is_active: bool
    created_on: datetime
