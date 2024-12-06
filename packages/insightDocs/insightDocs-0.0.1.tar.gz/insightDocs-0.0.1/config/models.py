from dataclasses import dataclass
from typing import Dict, Any, Optional
import uuid

@dataclass
class Document:
    """Represents a document with content and metadata."""
    id: str
    content: str
    metadata: Dict[str, Any]
    filepath: str

    @classmethod
    def create(cls, content: str, metadata: Dict[str, Any], filepath: str) -> 'Document':
        """Create a Document instance with a generated ID."""
        return cls(
            id=str(uuid.uuid4()),
            content=content,
            metadata=metadata,
            filepath=filepath
        )

@dataclass
class DocumentChunk:
    """Represents a chunk of a document after splitting."""
    id: str
    text: str
    metadata: Dict[str, Any]
    original_doc_id: str
    chunk_index: int
    total_chunks: int
    filepath: str
    window_metadata: Dict[str, Any] = None 

    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary format."""
        return {
            'id': self.id,
            'text': self.text,
            'metadata': {
                **self.metadata,
                'filepath': self.filepath,
                'chunk_index': self.chunk_index,
                'total_chunks': self.total_chunks,
                'original_doc_id': self.original_doc_id,
                'window_metadata': self.window_metadata 
            },

        }