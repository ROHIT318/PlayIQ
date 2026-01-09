from pydantic import BaseModel, EmailStr, SecretStr
from typing import List
from datetime import datetime

class ChatDetailsModel(BaseModel):
    chat_id: str
    user_id: str
    chat_name: str
    chat_msg: str
    chat_media: List[str]
    created_on: datetime

class UserAccountModel(BaseModel):
    user_id: str
    mail: EmailStr
    pswd: SecretStr
    is_active: bool
    created_on: datetime