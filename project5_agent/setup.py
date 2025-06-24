from setuptools import setup, find_packages

setup(
    name="duke_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "boto3",
        "tavily"
    ],
    author="Your Name",
    description="A Streamlit AI agent for answering Duke University questions using Tavily and Bedrock Llama 3.",
) 