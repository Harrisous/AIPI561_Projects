from setuptools import setup, find_packages

setup(
    name="bedrock_memory_chatbot",
    version="0.1.0",
    description="A Streamlit chatbot app using AWS Bedrock Llama 3 with local memory.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "boto3"
    ],
    entry_points={
        "console_scripts": [
            "run-chatbot=streamlit run app.py"
        ]
    },
) 