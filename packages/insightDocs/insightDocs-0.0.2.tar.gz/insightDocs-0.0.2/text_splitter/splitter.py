from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import Document as LlamaDocument, Node
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

from config.models import DocumentChunk, Document
from config.config import TextSplitterConfig
import logging


logger = logging.getLogger(__name__)

class TextSplitterService:
    """Service for Markdown text splitting with metadata enrichment."""

    def __init__(self, config: TextSplitterConfig):
        self.config = config
        self._initialize_parsers()

    def _initialize_parsers(self):
        """Initialize parsers and metadata processors."""
        self.markdown_parser = MarkdownNodeParser(
            chunk_size=max(100, min(8000, self.config.chunk_size)),  
            chunk_overlap=min(self.config.chunk_overlap, self.config.chunk_size // 2)
        )
        self.metadata_processor = MetadataReplacementPostProcessor(
            target_metadata_key=self.config.window_metadata_key
        )

    def split_document(self, document: Document) -> List[DocumentChunk]:
        """Split the Markdown document into chunks with enhanced metadata."""
        try:
            if document.content.strip().startswith('#'):
                return self._split_markdown_document(document)
            else:
                return []  
        except Exception as e:
            logger.error(f"Error splitting document {document.id}: {str(e)}")
            raise

    def _split_markdown_document(self, document: Document) -> List[DocumentChunk]:
        """Split a Markdown document into chunks."""
        llama_doc = LlamaDocument(
            text=document.content,
            metadata=document.metadata,
            id_=document.id
        )
        nodes = self.markdown_parser.get_nodes_from_documents([llama_doc])
        processed_nodes = self._process_nodes(nodes, document.metadata)

        return [
            self._create_enhanced_chunk(document, node, index, len(processed_nodes))
            for index, node in enumerate(processed_nodes)
        ]

    def _process_nodes(self, nodes: List[Node], base_metadata: Dict[str, Any]) -> List[Node]:
        """Attach document metadata to each node."""
        processed_nodes = []
        for node in nodes:
            node.metadata.update(base_metadata)
            processed_nodes.append(node)
        return processed_nodes

    def _create_enhanced_chunk(self, document: Document, node: Node, index: int, total_chunks: int) -> DocumentChunk:
        """Create a chunk with enhanced metadata."""
        return DocumentChunk(
            id=f"{document.id}_chunk_{index}",
            text=node.text,
            metadata={
                **document.metadata,
                "chunk_info": {
                    "index": index,
                    "total": total_chunks,
                    "strategy": self.config.strategy
                },
                "original_text": node.metadata.get(self.config.original_text_key, "")
            },
            filepath=document.filepath,
            original_doc_id=document.id,
            chunk_index=index,
            total_chunks=total_chunks
        )