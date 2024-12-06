# textfromimage/azure_openai.py
import os
from openai import AzureOpenAI
from .utils import get_image_data

_client = None

def init(api_key=None, api_base=None, deployment_name=None, api_version="2024-02-15-preview"):
    """
    Initialize Azure OpenAI client.
    
    Parameters:
    - api_key (str, optional): Azure OpenAI API key. If not provided, reads from AZURE_OPENAI_API_KEY env var.
    - api_base (str, optional): Azure OpenAI endpoint. If not provided, reads from AZURE_OPENAI_ENDPOINT env var.
    - deployment_name (str, optional): Model deployment name. If not provided, reads from AZURE_OPENAI_DEPLOYMENT env var.
    - api_version (str): API version to use (default: "2024-02-15-preview")
    """
    global _client
    
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    api_base = api_base or os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    if not all([api_key, api_base, deployment_name]):
        raise ValueError(
            "Azure OpenAI configuration must be provided either via parameters or environment variables:\n"
            "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT"
        )
    
    # Ensure api_base has the correct format
    if not api_base.endswith('/'):
        api_base += '/'
    
    _client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        base_url=f"{api_base}openai/deployments/{deployment_name}"
    )
    
    # Store deployment name for later use
    global _deployment_name
    _deployment_name = deployment_name

def get_description(image_url, prompt="What's in this image?", max_tokens=300, system_prompt="You are a helpful assistant."):
    """
    Get image description using Azure OpenAI's vision capabilities.
    
    Parameters:
    - image_url (str): URL of the image to analyze
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - system_prompt (str): System message to set assistant behavior
    
    Returns:
    - str: Generated description
    """
    if _client is None:
        init()
    
    encoded_image, _ = get_image_data(image_url)
    
    try:
        response = _client.chat.completions.create(
            model=_deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Azure OpenAI API request failed: {e}")
