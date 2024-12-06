# TextFromImage

![Python Version](https://img.shields.io/pypi/pyversions/textfromimage)
![PyPI Version](https://img.shields.io/pypi/v/textfromimage)
![License](https://img.shields.io/pypi/l/textfromimage)
![Downloads](https://img.shields.io/pypi/dm/textfromimage)

A powerful Python library for obtaining detailed descriptions of images using various AI models including OpenAI's GPT models, Azure OpenAI, and Anthropic Claude. Perfect for applications requiring image understanding, accessibility features, and content analysis.

## 🌟 Key Features

- 🤖 **Multiple AI Providers**: Support for OpenAI, Azure OpenAI, and Anthropic Claude
- 🔄 **Flexible Integration**: Easy-to-use API with multiple initialization options
- 🎯 **Custom Prompting**: Configurable prompts for targeted descriptions
- 🔑 **Secure Authentication**: Multiple authentication methods including environment variables
- 🛠️ **Model Selection**: Support for different model versions and configurations
- 📝 **Type Hints**: Full typing support for better development experience

## 📦 Installation

```bash
pip install textfromimage
```

## 🚀 Quick Start

### OpenAI Integration

```python
import textfromimage

# Initialize with API key
textfromimage.openai.init(api_key="your-openai-api-key")

# Get image description
image_url = 'https://example.com/image.jpg'
description = textfromimage.openai.get_description(image_url=image_url)
print(f"Description: {description}")
```

## 💡 Advanced Usage

### 🤖 Multiple Provider Support

```python
# Anthropic Claude Integration
textfromimage.claude.init(api_key="your-anthropic-api-key")
claude_description = textfromimage.claude.get_description(image_url=image_url)

# Azure OpenAI Integration
textfromimage.azure_openai.init(
    api_key="your-azure-openai-api-key",
    api_base="https://your-azure-endpoint.openai.azure.com/",
    deployment_name="your-deployment-name"
)
azure_description = textfromimage.azure_openai.get_description(image_url=image_url)
```

### 🔧 Configuration Options

```python
# Environment Variable Configuration
import os
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'
os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'
os.environ['AZURE_OPENAI_API_KEY'] = 'your-azure-openai-api-key'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'your-azure-endpoint'
os.environ['AZURE_OPENAI_DEPLOYMENT'] = 'your-deployment-name'

# Custom Model Selection
description = textfromimage.openai.get_description(
    image_url=image_url,
    model='gpt-4o-mini'
)

# Custom Prompting
description = textfromimage.openai.get_description(
    image_url=image_url,
    prompt="Describe the main elements and composition of this image"
)
```

## 📋 Parameters

```python
@dataclass
class DescriptionParams:
    image_url: str
    prompt: str = "What's in this image?"
    model: str = "gpt-4o"
    api_key: Optional[str] = None
```

## 🔍 Error Handling

```python
from textfromimage.exceptions import APIKeyError, InvalidImageError, ModelError

try:
    description = textfromimage.openai.get_description(image_url=image_url)
except APIKeyError as e:
    print(f"API key error: {e}")
except InvalidImageError as e:
    print(f"Image error: {e}")
except ModelError as e:
    print(f"Model error: {e}")
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.