from setuptools import setup, find_packages

setup(
    name="textfromimage",
    version="0.3.1",  # Incremented version for new features
    author="Oren Grinker",
    author_email="orengr4@gmail.com",
    description="Get descriptions of images from OpenAI, Azure OpenAI, and Anthropic Claude models in an easy way.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/OrenGrinker/textfromimage",
    packages=find_packages(),
    install_requires=[
        "openai>=1.35.15",
        "requests>=2.25.1",
        "anthropic>=0.18.1"
    ],
    extras_require={
        "azure": ["azure-identity>=1.15.0"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.9',
    keywords="openai gpt-4 claude azure-openai computer-vision image-to-text ai machine-learning",
)
