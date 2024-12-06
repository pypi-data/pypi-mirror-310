from typing import List
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from llama_index.core.embeddings import BaseEmbedding

class HuggingFaceEmbedding(BaseEmbedding, Embeddings):
    """Wrapper for HuggingFace embedding models to make them compatible with LangChain."""
   
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5", device: str = "cpu"):
        """Initialize the embedding model."""
        super().__init__()
        self._model = SentenceTransformer(model_name, device=device)
       
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        embeddings = self._model.encode(texts, convert_to_numpy=True).tolist()
        return embeddings
   
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query text."""
        return self._model.encode(text, convert_to_numpy=True).tolist()

    # LlamaIndex interface methods
    def _get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for a query string."""
        return self.embed_query(query)
    
    def _get_text_embedding(self, text: str) -> List[float]:
        """Get embedding for a text string."""
        return self.embed_query(text)
    
    async def _aget_query_embedding(self, query: str) -> List[float]:
        """Async version of query embedding."""
        return self._get_query_embedding(query)
    
    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Async version of text embedding."""
        return self._get_text_embedding(text)

def get_embedding_model(model_type: str = "huggingface", 
                       model_name: str = "BAAI/bge-base-en-v1.5", 
                       device: str = "cpu") -> Embeddings:
    """Get the appropriate embedding model based on type."""
    if model_type.lower() == "huggingface":
        return HuggingFaceEmbedding(model_name=model_name, device=device)
    else:
        raise ValueError(f"Unsupported embedding model type: {model_type}")