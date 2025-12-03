from pydantic import BaseModel
from typing import Optional, List

from models.UserInformation import UserInformation
from models.ChatHistory import ChatHistory

class ChatRequest(BaseModel):
    prompt: str
    platform: str
    user: Optional[UserInformation] = None