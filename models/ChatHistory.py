from pydantic import BaseModel
from typing import Optional

class ChatHistory(BaseModel):
    chat_id: Optional[int] = None
    role: str
    message: str
    #timestamp: Optional[str] = None