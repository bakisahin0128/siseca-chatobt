import os
from dotenv import load_dotenv

load_dotenv()

class MODEL_AZURE_OPENAI:
    API_VERSION = "2024-02-01"
    API_ENDPOINT = os.environ["OPENAI_API_BASE"]
    API_KEY = os.environ["OPENAI_API_KEY"]
    DEPLOYMENT_NAME = "gpt-4o"