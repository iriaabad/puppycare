from unittest.mock import Base
from pydantic import BaseModel


#definimos clase de TokenData
class TokenData (BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str