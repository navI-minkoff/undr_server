from pydantic import BaseModel
from typing import Optional


class TokenResponse(BaseModel):
    token: str
    token_type: str


class TokenValidationResponse(BaseModel):
    is_valid: bool
    user_id: Optional[int]
    message: str
