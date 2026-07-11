from pydantic import BaseModel, EmailStr

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