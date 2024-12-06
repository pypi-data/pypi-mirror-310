# textfromimage/openai.py
import os
from openai import OpenAI
from .utils import get_image_data

_client = None


def init(api_key=None):
    """
    Initialize OpenAI client with API key.

    Parameters:
    - api_key (str, optional): OpenAI API key. If not provided, reads from OPENAI_API_KEY env var.
    """
    global _client
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key must be provided via api_key parameter or OPENAI_API_KEY environment variable.")
    _client = OpenAI(api_key=api_key)


def get_description(image_url, prompt="What's in this image?", max_tokens=300, model="gpt-4o"):
    """
    Get image description using OpenAI's vision models.

    Parameters:
    - image_url (str): URL of the image to analyze
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - model (str): OpenAI model to use

    Returns:
    - str: Generated description
    """
    if _client is None:
        init()

    encoded_image, _ = get_image_data(image_url)

    try:
        response = _client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenAI API request failed: {e}")
