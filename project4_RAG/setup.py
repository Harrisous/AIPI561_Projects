from setuptools import setup, find_packages

setup(
    name='crystal_rag_chatbot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.25.0',
        'openai>=1.0.0',
        'pinecone>=3.0.0',
        'boto3>=1.28.0',
        'python-dotenv>=1.0.0',
        'tqdm>=4.0.0',
    ],
    entry_points={
        'console_scripts': [
            'crystal-rag-chatbot = streamlit_app:main'
        ]
    },
    author='Your Name',
    description='A Streamlit RAG chatbot for crystal recommendations using Pinecone and AWS Bedrock.',
    include_package_data=True,
    python_requires='>=3.8',
) 