from pydantic import BaseModel

class loginUser(BaseModel):
    email: str
    password: str
class onBoardUser(BaseModel):
    username: str
    email: str
    password: str