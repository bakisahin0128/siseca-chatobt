from typing import Optional, Mapping, List
from collections import defaultdict
from pydantic import BaseModel
from fastapi import status as http_status


class APIResponse(BaseModel):
    """
    Represents the structure of the API response returned by the chatbot endpoints.
    """
    status: str = "success"  # The status of the API response (default: "success")
    message: str = ""  # A descriptive message associated with the API response
    code: int = http_status.HTTP_200_OK  # The HTTP status code of the response (default: 200 OK)
    error: Optional[Mapping] = defaultdict(list)  # Any errors that occurred during the API call
    data: Optional[Mapping] = dict()  # The data returned by the API


class ChatResponse(APIResponse):
    """
    Represents the response format for the chatbot API.
    Inherits from the APIResponse class.
    """
    pass


class ChatRequest(BaseModel):
    """
    Represents the structure of the Chat request object sent to the chatbot endpoints.
    """
    input: str  # The input or query sent to the chatbot
    history: List = []  # The chat history
