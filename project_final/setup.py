from setuptools import setup, find_packages

setup(
    name='url-sentiment-analyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'requests',
        'boto3',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'run-app = app:main',
        ],
    },
    author='Your Name',
    description='A Streamlit app for sentiment analysis of URL content using Bedrock Llama 3.2 90B Vision Instruct.',
) 