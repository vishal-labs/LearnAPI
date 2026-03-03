from pydantic import BaseModel
from pydantic import EmailStr, constr

class loginUser(BaseModel):
    email: str
    password: str
class onBoardUser(BaseModel):
    username: str
    email: str
    password: str
class makeUserAdmin(BaseModel):
    email : EmailStr
    adminKey : str