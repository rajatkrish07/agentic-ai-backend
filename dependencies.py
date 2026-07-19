from datetime import datetime
from schemas import CurrentUser
from models import Chat, Message, AIResponse
from fastapi import HTTPException, Depends, Path
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
            Chat(
                id="chat_001",
                title="Python",
                messages=[

                    Message(
                        id="msg_001",
                        chat_id="chat_001",
                        timestamp=datetime.now(),
                        text="What is Python?",
                        responses=[
                            AIResponse(
                                id="resp_001",
                                text="Python is a high-level, interpreted programming language known for its readability, simplicity, and extensive ecosystem.",
                                created_at=datetime.now(),
                            )
                        ]
                    ),

                    Message(
                        id="msg_002",
                        chat_id="chat_001",
                        timestamp=datetime.now(),
                        text="Explain OOP.",
                        responses=[
                            AIResponse(
                                id="resp_002",
                                text="Object-Oriented Programming (OOP) organizes code into classes and objects, enabling encapsulation, inheritance, polymorphism, and abstraction.",
                                created_at=datetime.now(),
                            )
                        ]
                    )
                ]
            ),

            Chat(
                id="chat_002",
                title="FastAPI",
                messages=[

                    Message(
                        id="msg_003",
                        chat_id="chat_002",
                        timestamp=datetime.now(),
                        text="What is Dependency Injection?",
                        responses=[
                            AIResponse(
                                id="resp_003",
                                text="Dependency Injection is a design pattern where FastAPI automatically provides required objects or services to your endpoint functions.",
                                created_at=datetime.now(),
                            )
                        ]
                    ),

                    Message(
                        id="msg_004",
                        chat_id="chat_002",
                        timestamp=datetime.now(),
                        text="Explain Path Parameters.",
                        responses=[
                            AIResponse(
                                id="resp_004",
                                text="Path parameters are dynamic values embedded in a URL that allow endpoints to identify and operate on specific resources.",
                                created_at=datetime.now(),
                            )
                        ]
                    )
                ]
            ),

            Chat(
                id="chat_003",
                 title="RAG",
                 messages=[
                     Message(
                         id="msg_005",
                         chat_id="chat_003",
                         timestamp=datetime.now(),
                         text="What is Retrieval-Augmented Generation?",
                         responses=[
                             AIResponse(
                                 id="resp_005",
                                 text="Retrieval-Augmented Generation (RAG) combines information retrieval with large language models to produce more accurate and context-aware responses.",
                                 created_at=datetime.now(),
                             )
                         ]
                     ),
                     Message(
                         id="msg_006",
                         chat_id="chat_003",
                         timestamp=datetime.now(),
                         text="Explain Vector Databases.",
                         responses=[
                             AIResponse(
                                 id="resp_006",
                                 text="Vector databases store embeddings and enable efficient similarity search, making them essential for semantic search and RAG systems.",
                                 created_at=datetime.now(),
                             )
                         ]
                     ),
                 ]
            ),

            Chat(
                id="chat_004",
                title="Agents",
                messages=[

                     Message(
                         id="msg_007",
                         chat_id="chat_004",
                         timestamp=datetime.now(),
                         text="What are AI Agents?",
                         responses=[
                             AIResponse(
                                 id="resp_007",
                                 text="AI Agents are autonomous systems that perceive their environment, reason about goals, and take actions to accomplish tasks with minimal human intervention.",
                                 created_at=datetime.now(),
                             )
                         ]
                     ),

                     Message(
                         id="msg_008",
                         chat_id="chat_004",
                         timestamp=datetime.now(),
                         text="Explain Agentic Workflows.",
                         responses=[
                             AIResponse(
                                 id="resp_008",
                                 text="Agentic workflows combine planning, memory, reasoning, and tool usage to solve complex tasks through coordinated, multi-step execution.",
                                 created_at=datetime.now(),
                             )
                         ]
                     ),
                 ]
            ),
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

def get_message(
        message_id: str = Path(
            ...,
            min_length=1,
            title="Message ID",
            description="Unique identifier of the message",
            examples=["msg_001"]
        ),
        chat: Chat = Depends(get_chat)

) -> Message:

    for message in chat.messages:
        if message.id == message_id:
            return message

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Message with '{message_id}' is not found."
    )

