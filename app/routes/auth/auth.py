from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.models.user import User
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.config.db import get_database

router = APIRouter()

@router.post("/test")
async def health_check():
    return {"message": "Welcome to FastAPI MongoDB Project"}

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user: UserCreate):
    db = await get_database()
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    
    # Dump model to dict, exclude id (it will be created by Mongo)
    user_dict = new_user.model_dump(by_alias=True, exclude={"id"})
    
    result = await db["users"].insert_one(user_dict)
    
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    
    # Map _id to id for response
    return UserResponse(**created_user, id=str(created_user["_id"]))

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db = await get_database()
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/register")
async def register_get_error():
    return {"message": "You are performing a GET request (viewing in browser). Please use a POST request with 'email' and 'password' to register."}

@router.get("/login")
async def login_get_error():
    return {"message": "You are performing a GET request. Please use a POST request with 'email' and 'password' to login."}
