from enum import Enum
from typing import Optional, Union, Dict
from openai import OpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

class Provider(Enum):
    AZURE = "azure"
    OPENAI = "openai"

class ChatAssistant:
    def __init__(
        self,
        provider: Provider,
        api_key: str,
        model_name: str,
        azure_endpoint: Optional[str] = None
    ):
        """
        Initialize ChatAssistant with either OpenAI or Azure OpenAI.
        
        Args:
            provider (Provider): AZURE or OPENAI
            api_key (str): API key for the chosen provider
            model_name (str): Name of the model to use
            azure_endpoint (Optional[str]): Required only for Azure OpenAI
        """
        self.provider = provider
        self.model_name = model_name

        if provider == Provider.AZURE:
            if not azure_endpoint:
                raise ValueError("Azure endpoint is required for Azure OpenAI")
            self.client = AzureOpenAI(
                azure_endpoint = azure_endpoint, 
                api_key=api_key,  
                api_version="2024-02-01"
            )
        else:
            self.client = OpenAI(api_key=api_key)

    def get_response(
        self,
        query: str,
        system_message: str = "You are a helpful assistant.",
        temperature: float = 1.0,
        max_tokens: int = 2000
    ) -> Dict:
        """
        Get a response from the model.
        
        Args:
            query (str): User's input query
            system_message (str): System message for the assistant
            temperature (float): Controls randomness (0.0 to 2.0)
            max_tokens (int): Maximum tokens in response
            
        Returns:
            Dict: Response containing content and metadata
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]

        try:
            if self.provider == Provider.AZURE:
                from azure.ai.inference.models import SystemMessage, UserMessage
                azure_messages = [
                    SystemMessage(content=system_message),
                    UserMessage(content=query)
                ]
                
                response = self.client.chat.completions.create(
                    messages=azure_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=self.model_name
                )
                
                return {
                    "content": response.choices[0].message.content,
                    "usage": response.usage.model_dump(),
                    "finish_reason": response.choices[0].finish_reason
                }
            else:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                return {
                    "content": response.choices[0].message.content,
                    "usage": response.usage.model_dump(),
                    "finish_reason": response.choices[0].finish_reason,
                    "model": response.model
                }

        except Exception as e:
            raise RuntimeError(f"API error: {str(e)}")