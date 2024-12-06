# textfromimage/utils.py
import os
import base64
import requests
import mimetypes


def get_image_data(image_url):
    """
    Download and process image from URL.
    Returns base64 encoded image and content type.
    """
    response = requests.get(image_url)
    if response.status_code != 200:
        raise ValueError(f"Could not retrieve image from URL: {image_url}")

    # Get content type
    content_type = response.headers.get('content-type')
    if not content_type:
        content_type, _ = mimetypes.guess_type(image_url)
    if not content_type:
        content_type = 'image/jpeg'

    # Encode image
    encoded_image = base64.b64encode(response.content).decode('utf-8')

    return encoded_image, content_type