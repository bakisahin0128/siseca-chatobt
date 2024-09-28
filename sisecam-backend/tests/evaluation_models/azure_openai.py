from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_openai import AzureChatOpenAI
from evaluation_models.configuration import MODEL_AZURE_OPENAI
import os

class AzureOpenAI(DeepEvalBaseLLM):
    def __init__(
        self,
        model
    ):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Custom Azure OpenAI Model"

os.environ.pop('OPENAI_API_BASE', None)
os.environ.pop('OPENAI_API_KEY', None)

custom_model_azure = AzureChatOpenAI(
    azure_endpoint=MODEL_AZURE_OPENAI.API_ENDPOINT,
    azure_deployment=MODEL_AZURE_OPENAI.DEPLOYMENT_NAME,
    openai_api_version=MODEL_AZURE_OPENAI.API_VERSION,
    openai_api_key=MODEL_AZURE_OPENAI.API_KEY
)

AZURE_MODEL = AzureOpenAI(model=custom_model_azure)