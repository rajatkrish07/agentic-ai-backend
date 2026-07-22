import time
from dependencies import get_api_version, get_message
from models import UserAccount, Message, AIResponse
from schemas import UserResponse, AdminUserResponse, AIUserResponse ,GenerateAIResponse, RegenerateAIResponse, ResponseHistorySchema
from exceptions import UserNotFoundError, ChatNotFoundError, MessageNotFoundError, AIResponseNotFoundError
from fastapi import FastAPI, Query, Path, Header, Depends, Request
from fastapi.responses import JSONResponse
from starlette import status
from datetime import datetime

# app -> FastAPI Application object
app = FastAPI()

# Middleware - HTTP
@app.middleware("http")
async def log_requests(
        request: Request,
        call_next
):

    # Start time
    start_time = time.perf_counter()

    print(f"{request.method} {request.url.path}")
    response = await call_next(request)

    # End time
    end_time = time.perf_counter()

    response.headers["X-App-Name"] = "Cogentra"
    process_time = end_time - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f} seconds"
    return response

# Global Exception Handler (Domain Exception -> HTTP Response)

# For No User Found
@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(
    request: Request,
    exc: UserNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc)
        }
    )

# For No Chats Found
@app.exception_handler(ChatNotFoundError)
async def handle_chat_not_found(
    request: Request,
    exc: ChatNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc)
        }
    )

# For No Message Found
@app.exception_handler(ChatNotFoundError)
async def handle_message_not_found(
    request: Request,
    exc: MessageNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc)
        }
    )

# For No AI Response Found
@app.exception_handler(AIResponseNotFoundError)
async def handle_ai_response_not_found(
    request: Request,
    exc: AIResponseNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc)
        }
    )

# Different User Displays
@app.get("/admin/users", response_model=AdminUserResponse)
def admin_display(user: UserAccount):
    return user

@app.get("/users", response_model=UserResponse)
def user_display(user: UserAccount):
    return user

@app.get("/ai/users", response_model=AIUserResponse)
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

# Path Parameter

# Fetching user info by id

@app.get("/users/{user_id}")
def get_user(
        user_id: int = Path(
            ...,
            ge=1,
            title="User ID",
            description="Unique identifier of the user",
            examples=[1]
        )
):
    return {
        "requested_user": user_id
    }

# Fetching user info by name
@app.get("/users")
def search_users(
        name: str | None= Query(
            None,
            title="User Name",
            min_length=2,
            max_length=50,
            description="Search users by username",
        )):
    return {
        "searched_name": name
    }

# Header param
@app.get("/profile")
def profile(
        authorization: str = Header(
            ...,
            description="JWT Bearer Token"
        )
):
    return {
        "token": authorization
    }

# Generates the message
@app.post("/chats/{chat_id}/messages/{message_id}/generate", response_model=GenerateAIResponse, status_code=status.HTTP_201_CREATED)
def create_ai_response(
    version: str = Depends(get_api_version),
    message: Message = Depends(get_message)
):

    return {
        "chat_id": message.chat_id,
        "message_id": message.id,
        "user_prompt": message.text,
        "ai_response": "Dependency Injection allows...",
        "version": version
    }

# Regenerates the response and adds it to a list for persistence
@app.post("/chats/{chat_id}/messages/{message_id}/regenerate",response_model=RegenerateAIResponse, status_code=status.HTTP_201_CREATED)
def regenerate_ai_response(
        message: Message = Depends(get_message)
):
    new_response = AIResponse(
        id="resp_009",
        text="This is a regenerated AI response.",
        created_at=datetime.now()
    )

    message.responses.append(new_response)

    return{
        "message": "AI response regenerated successfully.",
        "response": new_response
    }


# Displays all the responses generated
@app.get("/chats/{chat_id}/messages/{message_id}/responses", response_model=ResponseHistorySchema, status_code=status.HTTP_200_OK)
def get_response_history(
        message: Message = Depends(get_message)
):

    return{
        "message": "Responses retrieved successfully.",
        "responses": message.responses
    }
