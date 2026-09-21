from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.auth.service import register_user, login_user
from app.auth.schema import UserResponse, UserCreate, UserLogin, Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
  prefix="/auth",
  tags=["Auth"]
)

@router.post("/register", response_model=UserResponse)
async def create_user(data: UserCreate):
  return await register_user(data)

@router.post("/login", response_model=Token)
async def user_login(formData = Depends(OAuth2PasswordRequestForm)):
  data = UserLogin(
    email = formData.username,
    password = formData.password
  )
  return await login_user(data)

@router.get("/profile")
async def profile(current_user = Depends(get_current_user)):
  return current_user