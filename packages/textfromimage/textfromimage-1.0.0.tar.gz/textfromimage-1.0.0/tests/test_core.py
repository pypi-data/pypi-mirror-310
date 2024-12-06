# tests/test_core.py

import unittest
from unittest.mock import patch, MagicMock
from textfromimage import openai as openai_module
from textfromimage import azure_openai as azure_openai_module
from textfromimage import claude as claude_module
import os


class TestOpenAI(unittest.TestCase):
    """Tests for the OpenAI backend of TextFromImage."""

    @patch('textfromimage.openai.requests.get')
    @patch('textfromimage.openai.OpenAI')
    def test_get_description_invalid_url(self, mock_openai_client, mock_requests_get):
        """
        Test that providing an invalid image URL raises a ValueError for OpenAI backend.
        """
        # Mock the HTTP GET request to return a 404 status code
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Initialize OpenAI client with a dummy API key
        openai_module.init(api_key="dummy_openai_api_key")

        with self.assertRaises(ValueError):
            openai_module.get_description('invalid_url')

    @patch('textfromimage.openai.requests.get')
    def test_get_description_no_api_key(self, mock_requests_get):
        """
        Test that omitting the API key raises a ValueError for OpenAI backend.
        """
        # Backup the original OPENAI_API_KEY environment variable
        original_api_key = os.environ.get('OPENAI_API_KEY')

        try:
            # Ensure the OPENAI_API_KEY environment variable is unset
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']

            # Initialize OpenAI client without an API key
            with self.assertRaises(ValueError):
                openai_module.init()
        finally:
            # Restore the original API key if it was set
            if original_api_key is not None:
                os.environ['OPENAI_API_KEY'] = original_api_key

    @patch('textfromimage.openai.requests.get')
    @patch('textfromimage.openai.OpenAI')
    def test_get_description_success(self, mock_openai_client, mock_requests_get):
        """
        Test successful retrieval of image description using OpenAI backend.
        """
        # Mock the HTTP GET request to return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        # Mock the OpenAI client's chat completions response
        mock_chat = MagicMock()
        mock_chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test description from OpenAI."))]
        )
        mock_openai_client.return_value = MagicMock(chat=mock_chat)

        # Initialize OpenAI client with a dummy API key
        openai_module.init(api_key="dummy_openai_api_key")

        description = openai_module.get_description('https://example.com/image.jpg')
        self.assertEqual(description, "Test description from OpenAI.")


class TestAzureOpenAI(unittest.TestCase):
    """Tests for the Azure OpenAI backend of TextFromImage."""

    @patch('textfromimage.azure_openai.requests.get')
    @patch('textfromimage.azure_openai.AzureOpenAI')
    def test_get_description_invalid_url(self, mock_azure_client, mock_requests_get):
        """
        Test that providing an invalid image URL raises a ValueError for Azure OpenAI backend.
        """
        # Mock the HTTP GET request to return a 404 status code
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Initialize Azure OpenAI client with dummy credentials
        azure_openai_module.init(
            api_key="dummy_azure_api_key",
            api_base="https://dummy-azure-endpoint.openai.azure.com/",
            deployment_name="dummy-deployment"
        )

        with self.assertRaises(ValueError):
            azure_openai_module.get_description('invalid_url')

    @patch('textfromimage.azure_openai.requests.get')
    def test_get_description_no_api_key(self, mock_requests_get):
        """
        Test that omitting the API key raises a ValueError for Azure OpenAI backend.
        """
        # Backup the original Azure environment variables
        original_api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        original_api_base = os.environ.get('AZURE_OPENAI_ENDPOINT')
        original_deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT')

        try:
            # Ensure Azure environment variables are unset
            if 'AZURE_OPENAI_API_KEY' in os.environ:
                del os.environ['AZURE_OPENAI_API_KEY']
            if 'AZURE_OPENAI_ENDPOINT' in os.environ:
                del os.environ['AZURE_OPENAI_ENDPOINT']
            if 'AZURE_OPENAI_DEPLOYMENT' in os.environ:
                del os.environ['AZURE_OPENAI_DEPLOYMENT']

            # Initialize Azure OpenAI client without required credentials
            with self.assertRaises(ValueError):
                azure_openai_module.init()
        finally:
            # Restore the original Azure environment variables
            if original_api_key is not None:
                os.environ['AZURE_OPENAI_API_KEY'] = original_api_key
            if original_api_base is not None:
                os.environ['AZURE_OPENAI_ENDPOINT'] = original_api_base
            if original_deployment is not None:
                os.environ['AZURE_OPENAI_DEPLOYMENT'] = original_deployment

    @patch('textfromimage.azure_openai.requests.get')
    @patch('textfromimage.azure_openai.AzureOpenAI')
    def test_get_description_success(self, mock_azure_client, mock_requests_get):
        """
        Test successful retrieval of image description using Azure OpenAI backend.
        """
        # Mock the HTTP GET request to return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/png'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        # Mock the Azure OpenAI client's chat completions response
        mock_chat = MagicMock()
        mock_chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test description from Azure OpenAI."))]
        )
        mock_azure_client.return_value = MagicMock(chat=mock_chat)

        # Initialize Azure OpenAI client with dummy credentials
        azure_openai_module.init(
            api_key="dummy_azure_api_key",
            api_base="https://dummy-azure-endpoint.openai.azure.com/",
            deployment_name="dummy-deployment"
        )

        description = azure_openai_module.get_description('https://example.com/image.jpg')
        self.assertEqual(description, "Test description from Azure OpenAI.")


class TestClaude(unittest.TestCase):
    """Tests for the Anthropic Claude backend of TextFromImage."""

    @patch('textfromimage.claude.requests.get')
    @patch('textfromimage.claude.Anthropic')
    def test_get_description_invalid_url(self, mock_claude_client, mock_requests_get):
        """
        Test that providing an invalid image URL raises a ValueError for Claude backend.
        """
        # Mock the HTTP GET request to return a 404 status code
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Initialize Claude client with a dummy API key
        claude_module.init(api_key="dummy_claude_api_key")

        with self.assertRaises(ValueError):
            claude_module.get_description('invalid_url')

    @patch('textfromimage.claude.requests.get')
    def test_get_description_no_api_key(self, mock_requests_get):
        """
        Test that omitting the API key raises a ValueError for Claude backend.
        """
        # Backup the original ANTHROPIC_API_KEY environment variable
        original_api_key = os.environ.get('ANTHROPIC_API_KEY')

        try:
            # Ensure the ANTHROPIC_API_KEY environment variable is unset
            if 'ANTHROPIC_API_KEY' in os.environ:
                del os.environ['ANTHROPIC_API_KEY']

            # Initialize Claude client without an API key
            with self.assertRaises(ValueError):
                claude_module.init()
        finally:
            # Restore the original API key if it was set
            if original_api_key is not None:
                os.environ['ANTHROPIC_API_KEY'] = original_api_key

    @patch('textfromimage.claude.requests.get')
    @patch('textfromimage.claude.Anthropic')
    def test_get_description_success(self, mock_claude_client, mock_requests_get):
        """
        Test successful retrieval of image description using Anthropic Claude backend.
        """
        # Mock the HTTP GET request to return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        # Mock the Claude client's messages.create response
        mock_messages = MagicMock()
        mock_messages.create.return_value = MagicMock(
            content=[MagicMock(text="Test description from Claude.")]
        )
        mock_claude_client.return_value = MagicMock(messages=mock_messages)

        # Initialize Claude client with a dummy API key
        claude_module.init(api_key="dummy_claude_api_key")

        description = claude_module.get_description('https://example.com/image.jpg')
        self.assertEqual(description, "Test description from Claude.")


if __name__ == '__main__':
    unittest.main()
