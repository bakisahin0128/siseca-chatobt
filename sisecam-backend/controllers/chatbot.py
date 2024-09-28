from models.chatbot import ChatModel
from fastapi import status as http_status, HTTPException


class ChatController:
    """
    ChatController handles the logic for interacting with the ChatModel.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        model (ChatModel): Instance of the ChatModel.

    """

    __name__ = 'Chat'

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the ChatController.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.model = ChatModel()

    def chat(self, *args, **kwargs):
        """
        Sends a chat message to the ChatModel for processing.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ChatResponse: The response object containing the status and data.
                status (str): The status of the response.
                data (dict): A dictionary containing the user's input and the generated response.

        """
        if kwargs.get('input') is not None and kwargs.get('input').strip() != "":
            response = self.model.chat(*args, **kwargs)
            return response
        else:
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST,
                                detail="Provided input is empty or invalid!")
