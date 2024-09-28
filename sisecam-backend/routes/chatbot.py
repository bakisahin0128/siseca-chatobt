from fastapi import status as http_status, HTTPException, APIRouter, Request
from models import ChatRequest, ChatResponse
from controllers.chatbot import ChatController
from config import AUTHORIZATION_TOKEN

router = APIRouter(
    tags=["chatbot"],
    dependencies=[],
    responses={404: {"status": "error", "error": "Not found"}}
)


@router.post("/chat", response_model=ChatResponse)
async def chat(req: Request, chat_request: ChatRequest):
    """
    POST endpoint for chating with the chatbot.

    - `req`: Request object including Headers for authorization purposes.
    - `chat_request`: Request object containing the user's input and the session chat history.
        - `input`: String
        - `history`: List

    This endpoint allows the client to send a question to the chatbot
    and receives the response in the `response_model`.

    Returns:
        - `ChatResponse`: Response object containing the chatbot's answer to the question.

    """
    authorization = req.headers.get("authorization-token")
    if authorization != AUTHORIZATION_TOKEN:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")
    else:
        chat_ctrl = ChatController()
        response = chat_ctrl.chat(
            input=chat_request.input.replace("'", "\'").replace('"', '\"'),
            history=chat_request.history
        )
        return response
