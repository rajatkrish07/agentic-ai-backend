from models import *
from schemas import *
from fastapi import FastAPI, Query

# app -> FastAPI Application object
app = FastAPI()

# Exposes fields relevant for admin only
class UserResponse(BaseModel):
    username: str
    full_name: str

class AdminUserResponse(BaseModel):
    username: str
    email: EmailStr
    chat_count: int

class AIResponse(BaseModel):
    username: str
    chat_count: int

@app.post("/admin/users", response_model=AdminUserResponse)
def admin_display(user: UserAccount):
    return user

@app.post("/user", response_model=UserResponse)
def user_display(user: UserAccount):
    return user

@app.post("/ai/users", response_model=AIResponse)
def ai_display(user: UserAccount):
    return user

# Welcome page
@app.get("/")
def welcome_user():
    return {"message": "Welcome User!"}

# App's health check
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "cogentra"
    }

# Fetching user info by id
@app.get("/users/id/{user_id}")
def get_user(user_id: int):
    return {
        "requested user": user_id
    }

# Fetching user info by name
@app.get("/users/name/{name}")
def get_user_by_name(name: str):
    return {
        "requested user's name": name
    }

# Finding details based on name using query parameter
@app.get("/users")
def search_user(name: str = "Guest"):
    return {
        "search_name": name
    }

@app.get("/users/search")
def search_user(name: str =Query(
    ...,
    min_length=3,
    max_length=50,
    description="Search users by username",
    example="Rajat Krishnan"
)):
    return{
        "search_name": name
    }




