from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.config import settings
from jose import jwt, JWTError
from app.database.database import users_collection
from app.auth.schema import UserResponse

oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth_schema))-> UserResponse:

  try:
    jwt_decoded = jwt.decode(token, settings.secret_key,algorithms=[settings.algorithm])
  except JWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="The current user is not authorized")
  
  user_email = jwt_decoded["sub"]

  current_user = await users_collection.find_one({"email" : user_email})

  if not current_user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Token Payload"
    )

  return UserResponse(
    id=str(current_user["_id"]),
    name=current_user["name"],
    email=current_user["email"],
    role=current_user["role"],
    id_number=current_user["id_number"],
    address=current_user["address"]
  )

def require_roles(*allowed_roles):
  async def role_checker(current_user = Depends(get_current_user)):
    if current_user.role not in allowed_roles:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient Permissions"
      )
    return current_user
  return role_checker