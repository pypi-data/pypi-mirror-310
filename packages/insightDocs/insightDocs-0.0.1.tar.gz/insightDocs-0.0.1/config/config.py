from dataclasses import dataclass, field
from typing import Dict, Optional, List

@dataclass
class ChromaConfig:
    """Configuration for Chroma vector store."""
    collection_name: str
    persist_directory: str = "chroma"
    embedding_model_type: str = "huggingface"
    embedding_model_name: str = "BAAI/bge-base-en-v1.5"
    embedding_device: str = "cpu"
    distance_metric: str = "cosine"
    metadata_fields: List[str] = field(default_factory=lambda: [
        "space_key", "source", "original_doc_id", "chunk_index", "filepath"
    ])
    hnsw_construction_ef: int = 200,
    hnsw_search_ef: int = 100,      
    hnsw_m: int = 64 

@dataclass
class TextSplitterConfig:
    """Configuration for enhanced text splitting with window context"""
    chunk_size: int = 1000
    chunk_overlap: int = 100
    window_size: int = 3
    window_metadata_key: str = "window"
    original_text_key: str = "original_text"
    similarity_top_k: int = 2
    strategy: str = "sentence_window" 