from schemas import CurrentUser
from models import Chat
from fastapi import Depends, Path
from fastapi import HTTPException
from starlette import status

# Returns API Version
def get_api_version() -> str:
    return "v1"

# Validates Current User
def get_curr_user() -> CurrentUser:
    return CurrentUser(
        username="rajatkr_07",
        email="rajatkrishnan2002@gmail.com",
        chats=[
            Chat(id="chat_001", title="Python", messages=[]),
            Chat(id="chat_002", title="FastAPI", messages=[]),
            Chat(id="chat_003", title="RAG", messages=[]),
            Chat(id="chat_004", title="Agents", messages=[]),
        ]
    )

def get_chat(
        chat_id: str = Path(
            ...,
            min_length=1,
            title="Chat ID",
            description="Unique identifier of the chat",
            examples=["chat_001"]
        ),
        curr_user: CurrentUser = Depends(get_curr_user)
) -> Chat:

    for chat in curr_user.chats:
        if chat.id == chat_id:
            return chat

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Chat ID with '{chat_id}' is not found."
    )

