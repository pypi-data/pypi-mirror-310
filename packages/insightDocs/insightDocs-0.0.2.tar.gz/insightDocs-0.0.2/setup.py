from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'RAG'
LONG_DESCRIPTION = 'description'

setup(
    name="insightDocs", 
    version=VERSION,
    author="devashish",
    author_email="jadhavom263@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=["confluence", "database", "embedding", "text_splitter", "config"]),
    install_requires=[
        "chromadb",
        "beautifulsoup4",
        "transformers",
        "aiohttp",
        "asyncio",
        "python-dotenv",
        "llama-index",
        "sentence-transformers",
        "torch",
        "llama-index-vector-stores-chroma",
        "llama-index-embeddings-huggingface",
        "llama-index-embeddings-instructor",
        "langchain",
        "langchain-community",
        "azure-ai-inference",
        "pymongo",
        "llama-index-vector-stores-azurecosmosmongo",
        "llama-index-embeddings-langchain",
        "tiktoken",
        "openai",
        "httptools"
    ],
    keywords=['python', 'rag'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
