# textfromimage/claude.py
import os
from anthropic import Anthropic
from .utils import get_image_data

_client = None


def init(api_key=None):
    """
    Initialize Claude client with API key.

    Parameters:
    - api_key (str, optional): Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var.
    """
    global _client
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "Anthropic API key must be provided via api_key parameter or ANTHROPIC_API_KEY environment variable.")
    _client = Anthropic(api_key=api_key)


def get_description(image_url, prompt="What's in this image?", max_tokens=300, model="claude-3-sonnet-20240229"):
    """
    Get image description using Claude's vision capabilities.

    Parameters:
    - image_url (str): URL of the image to analyze
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - model (str): Claude model to use

    Returns:
    - str: Generated description
    """
    if _client is None:
        init()

    encoded_image, media_type = get_image_data(image_url)

    try:
        response = _client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        raise RuntimeError(f"Claude API request failed: {e}")