from pydantic import BaseModel
from typing import Optional

class UserInformation(BaseModel):
    user_id: Optional[int] = None,
    full_name: Optional[str] = None,
    role: Optional[str] = None,
    company: Optional[str] = None,
    mobile: Optional[str] = None