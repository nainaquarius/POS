from pydantic import BaseModel
from typing import Literal

Role = Literal["admin", "manager", "cashier"]

class UserCreate(BaseModel):
  name: str
  email: str
  password: str
  id_number: str
  address: str

class UserLogin(BaseModel):
  email: str
  password: str

class UserResponse(BaseModel):
  id: str
  name: str
  email: str
  role: Role
  id_number: str
  address: str

class Token(BaseModel):
  access_token: str
  token_type: str