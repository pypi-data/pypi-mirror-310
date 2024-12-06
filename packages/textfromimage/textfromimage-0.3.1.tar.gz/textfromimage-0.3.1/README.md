# TextFromImage

Get descriptions of images using OpenAI's GPT models, Azure OpenAI, and Anthropic Claude in an easy way.

## Installation
You can install the textfromimage package via PyPI using pip:
```bash
pip install textfromimage
```

## Usage
The textfromimage package is now class-based, allowing you to initialize the TextFromImage class with your desired configurations and use its methods to obtain image descriptions.

**Using OpenAI**
```bash
import textfromimage

# Option 1: Initialize OpenAI client with API key
textfromimage.openai.init(api_key="your-openai-api-key")

# Option 2: Set your OpenAI API key as an environment variable
# import os
# os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'

# Get a description of the image using OpenAI
image_url = 'https://example.com/image.jpg'
openai_description = textfromimage.openai.get_description(
    image_url=image_url"
)
print("OpenAI Description:", openai_description)
```

**Using Anthropic Claude**
```bash
import textfromimage

# Option 1: Initialize Anthropic Claude client with API key
textfromimage.claude.init(api_key="your-anthropic-api-key")

# Option 2: Set your Anthropic API key as an environment variable
# import os
# os.environ['ANTHROPIC_API_KEY'] = 'your-anthropic-api-key'

# Get a description of the image using Anthropic Claude
image_url = 'https://example.com/image.jpg'
claude_description = textfromimage.claude.get_description(
    image_url=image_url"
)
print("Claude Description:", claude_description)
```

**Using Azure OpenAI**
```bash
import textfromimage

# Option 1: Initialize Azure OpenAI client with necessary parameters
textfromimage.azure_openai.init(
    api_key="your-azure-openai-api-key",
    api_base="https://your-azure-endpoint.openai.azure.com/",
    deployment_name="your-deployment-name"
)

# Option 2: Set your Azure OpenAI credentials as environment variables
# import os
# os.environ['AZURE_OPENAI_API_KEY'] = 'your-azure-openai-api-key'
# os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://your-azure-endpoint.openai.azure.com/'
# os.environ['AZURE_OPENAI_DEPLOYMENT'] = 'your-deployment-name'

# Get a description of the image using Azure OpenAI
image_url = 'https://example.com/image.jpg'
azure_description = textfromimage.azure_openai.get_description(
    image_url=image_url"
)
print("Azure OpenAI Description:", azure_description)
```

**Specifying a Different Model**

You can specify a different OpenAI model if needed. By default, the model is set to "gpt-4o".
```bash
import textfromimage

# Option 1: Initialize OpenAI client with API key
textfromimage.openai.init(api_key="your-openai-api-key")

# Option 2: Set your OpenAI API key as an environment variable
# import os
# os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'

# Get a description of the image using OpenAI
image_url = 'https://example.com/image.jpg'
openai_description = textfromimage.openai.get_description(
    image_url=image_url,
    model='gpt-4o-mini'"
)
print("OpenAI Description:", openai_description)
```

## Parameters

- image_url (str): The URL of the image.
- prompt (str, optional): The prompt for the description (default: "What's in this image?").
- model (str, optional): The OpenAI model to use (default: "gpt-4o").
- api_key (str, optional): Your OpenAI API key.


## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.