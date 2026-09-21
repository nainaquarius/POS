from app.database.database import users_collection
from fastapi import HTTPException, status
from app.auth.utils import hash_password, verify_password,create_access_token
from app.auth.schema import UserCreate, UserLogin, UserResponse, Token

async def register_user(user: UserCreate):
  user_exists = await users_collection.find_one({"email" : user.email})

  if user_exists:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="User Already Exists"
    )
  hashed_password = hash_password(user.password)

  new_user = {
    "name": user.name,
    "email" : user.email,
    "password" : hashed_password,
    "role" : "cashier",
    "id_number" : user.id_number,
    "address" : user.address
  }

  insert_result = await users_collection.insert_one(new_user)

  return UserResponse(
    id=str(insert_result.inserted_id),
    name=user.name,
    email=user.email,
    role="cashier",
    id_number=user.id_number,
    address=user.address
  )

async def login_user(data: UserLogin) -> Token:

  result = await users_collection.find_one({"email" : data.email})

  if not result:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Email or Password"
    )

  verified_password = verify_password(data.password, result["password"])

  if not verified_password:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Email or Password"
    )

  token = create_access_token({
    "sub" : result["email"]
  })

  return Token(
    token_type="bearer",
    access_token=token
  )