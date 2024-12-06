import json
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import chromadb
from langchain_community.vectorstores import Chroma
import logging
from chromadb.config import Settings as ChromaSettings
from tqdm.auto import tqdm

from embedding.embedding_manager import get_embedding_model
from config.models import DocumentChunk, Document
from config.config import ChromaConfig

logger = logging.getLogger(__name__)



class ChromaService:
    """Service for managing document chunks in Chroma vector store."""
    
    def __init__(self, config: ChromaConfig):
        self.config = config
        self._client = None
        self._collection = None
        self.embeddings = self._initialize_embeddings()
        
    def _initialize_embeddings(self):
        """Initialize the embedding model."""
        return get_embedding_model(
            model_type=self.config.embedding_model_type,
            model_name=self.config.embedding_model_name,
            device=self.config.embedding_device
        )

    @property
    def client(self):
        """Lazy initialization of Chroma client."""
        if self._client is None:
            client_settings = ChromaSettings(
                persist_directory=self.config.persist_directory,
                is_persistent=True,
                anonymized_telemetry=False,
                allow_reset=True,
                hnsw_config={
                    "space": "cosine",
                    "construction_ef": 400,
                    "search_ef": 200,
                    "M": 128
                }
            )
            
            try:
                self._client = chromadb.PersistentClient(
                    path=self.config.persist_directory,
                    settings=client_settings
                )
                logger.info(f"Initialized Chroma client with persist directory: {self.config.persist_directory}")
            except Exception as e:
                logger.error(f"Failed to initialize Chroma client: {str(e)}")
                raise
                
        return self._client

    @property
    def collection(self):
        """Lazy initialization of Chroma collection."""
        if self._collection is None:
            try:
                # Don't delete existing collection by default
                try:
                    self._collection = Chroma(
                        client=self.client,
                        collection_name=self.config.collection_name,
                        embedding_function=self.embeddings,
                        persist_directory=self.config.persist_directory,
                    )
                    logger.info(f"Loaded existing collection: {self.config.collection_name}")
                except Exception:
                    # Create new collection if it doesn't exist
                    self._collection = Chroma(
                        client=self.client,
                        collection_name=self.config.collection_name,
                        embedding_function=self.embeddings,
                        persist_directory=self.config.persist_directory,
                    )
                    logger.info(f"Created new collection: {self.config.collection_name}")
                
            except Exception as e:
                logger.error(f"Error initializing Chroma collection: {str(e)}")
                raise
                
        return self._collection

    async def store_chunks(self, chunks: List[DocumentChunk], batch_size: int = 100) -> None:
        """Store document chunks in Chroma with batching and progress bar."""
        try:
            total_batches = (len(chunks) + batch_size - 1) // batch_size
            
            with tqdm(total=total_batches, desc="Processing batches") as pbar:
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]
                    
                    texts = [chunk.text for chunk in batch]
                    metadatas = [self._prepare_metadata(chunk) for chunk in batch]
                    ids = [chunk.id for chunk in batch]
                    
                    # Add to Chroma
                    self.collection.add_texts(
                        texts=texts,
                        metadatas=metadatas,
                        ids=ids
                    )
                    
                    # Persist after each batch
                    self.collection.persist()
                    
                    pbar.update(1)
                    logger.debug(f"Stored batch {i//batch_size + 1}/{total_batches}")
                
            logger.info(f"Successfully stored {len(chunks)} chunks in {total_batches} batches")
                
        except Exception as e:
            logger.error(f"Error storing chunks in Chroma: {str(e)}")
            raise

    def retrieve_chunks(self, query: str, top_k: int = 5, score_threshold: float = 0.5) -> List[Dict]:
        """Retrieve top-k most similar document chunks based on a query."""
        try:
            search_params = {
                "ef": 200,  
                "k": min(top_k * 2, 100) 
            }
            # First check if collection is empty
            if self.collection._collection.count() == 0:
                logger.warning("Collection is empty. No documents to search.")
                return []

            # Log the query embedding for debugging
            query_embedding = self.embeddings.embed_query(query)
            logger.debug(f"Generated query embedding of length {len(query_embedding)}")
            
            # Use similarity_search_with_score with score threshold
            results = self.collection.similarity_search_with_score(
                query=query,
                k=search_params["k"]
            )
            
            # Filter and format results
            retrieved_chunks = []
            for doc, score in results:
                if score <= score_threshold:  
                    chunk = {
                        "text": doc.page_content,
                        "metadata": doc.metadata,
                        "score": score
                    }
                    retrieved_chunks.append(chunk)
                    logger.debug(f"Retrieved chunk with score {score:.4f}")
            
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: {query}")
            return retrieved_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving chunks for query '{query}': {str(e)}")
            raise

    def reset_collection(self) -> None:
        """Reset the collection by deleting and recreating it."""
        try:
            if self._collection is not None:
                self.client.delete_collection(name=self.config.collection_name)
                logger.info(f"Deleted collection: {self.config.collection_name}")
                self._collection = None  # Force recreation on next access
                
            # Access collection property to create new collection
            _ = self.collection
            logger.info("Successfully reset collection")
            
        except Exception as e:
            logger.error(f"Error resetting collection: {str(e)}")
            raise

    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection."""
        try:
            count = self.collection._collection.count()
            return {
                "total_documents": count,
                "collection_name": self.config.collection_name,
                "persist_directory": self.config.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            raise
        
    def _initialize_embeddings(self):
        """Initialize the embedding model."""
        return get_embedding_model(
            model_type=self.config.embedding_model_type,
            model_name=self.config.embedding_model_name,
            device=self.config.embedding_device
        )

    @property
    def client(self):
        """Lazy initialization of Chroma client."""
        if self._client is None:
            client_settings = ChromaSettings(
                persist_directory=self.config.persist_directory,
                is_persistent=True,
                anonymized_telemetry=False
            )
            
            try:
                self._client = chromadb.PersistentClient(
                    path=self.config.persist_directory,
                    settings=client_settings
                )
            except Exception as e:
                logger.error(f"Failed to initialize Chroma client: {str(e)}")
                raise
                
        return self._client

    @property
    def collection(self):
        """Lazy initialization of Chroma collection."""
        if self._collection is None:
            try:
                hnsw_config = {
                    "hnsw:space": "cosine",  
                    "hnsw:construction_ef": 400, 
                    "hnsw:search_ef": 200,      
                    "hnsw:M": 128              
                }
                try:
                    existing_collection = self.client.get_collection(
                        name=self.config.collection_name,
                    )
                except Exception:
                    logger.error(f"Failed to initialize Chroma client: {str(e)}")
                    raise
                
                self._collection = Chroma(
                    client=self.client,
                    collection_name=self.config.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=self.config.persist_directory,
                )
                
                logger.info(f"Successfully initialized collection: {self.config.collection_name}")
                
            except Exception as e:
                logger.error(f"Error initializing Chroma collection: {str(e)}")
                raise
                
        return self._collection

    def _prepare_metadata(self, chunk: DocumentChunk) -> Dict:
        """Prepare metadata for storage."""
        metadata = {
            "chunk_id": chunk.id,
            "original_doc_id": chunk.original_doc_id,
            "filepath": chunk.metadata.get("filepath", ""),
            "chunk_index": chunk.chunk_index,
            "total_chunks": chunk.total_chunks,
        }
        
        if chunk.window_metadata:
            metadata["has_window_context"] = True
            metadata["window_size"] = chunk.window_metadata.get("window_size", 0)
            metadata["prev_context_count"] = len(chunk.window_metadata.get("previous_context", []))
            metadata["next_context_count"] = len(chunk.window_metadata.get("next_context", []))
            
            
            prev_texts = [ctx["text"][:100] for ctx in chunk.window_metadata.get("previous_context", []) if isinstance(ctx, dict) and "text" in ctx]
            next_texts = [ctx["text"][:100] for ctx in chunk.window_metadata.get("next_context", []) if isinstance(ctx, dict) and "text" in ctx]
            metadata["context_summary"] = json.dumps({
                "previous": prev_texts,
                "next": next_texts
            })
        
        for field in self.config.metadata_fields:
            if field in chunk.metadata:
                metadata[field] = chunk.metadata[field]
                
        return metadata

    def retrieve_chunks_with_document_context(self, query: str, top_k: int = 20, score_threshold: float = 0.5) -> List[Dict]:
        """Retrieve top-k most similar document chunks based on a query, including surrounding document chunks."""
        try:
            if self.collection._collection.count() == 0:
                logger.warning("Collection is empty. No documents to search.")
                return []

            adjusted_k = min(top_k, self.collection._collection.count())

            try:
                results = self.collection.similarity_search_with_score(
                    query=query,
                    k=adjusted_k
                )
            except Exception as e:
                logger.warning(f"Initial similarity search failed. Attempting with reduced k. Error: {str(e)}")
                results = self.collection.similarity_search_with_score(
                    query=query,
                    k=min(10, self.collection._collection.count())
                )

            retrieved_chunks = []
            for doc, score in results:
                if score <= score_threshold:
                    metadata = doc.metadata
                    doc_id = metadata.get('original_doc_id')
                    chunk_index = metadata.get('chunk_index')
                    total_chunks = metadata.get('total_chunks')
                    
                    # Find surrounding chunks from the same document
                    surrounding_chunks = []
                    if doc_id and chunk_index is not None and total_chunks:
                        # Search for previous chunk
                        if chunk_index > 0:
                            try:
                                prev_results = self.collection.similarity_search_with_score(
                                    query="", 
                                    k=1,
                                    filter={
                                        "$and": [
                                            {"original_doc_id": {"$eq": doc_id}},
                                            {"chunk_index": {"$eq": chunk_index - 1}}
                                        ]
                                    }
                                )
                                if prev_results:
                                    surrounding_chunks.append({
                                        "text": prev_results[0][0].page_content,
                                        "type": "previous",
                                        "index": chunk_index - 1
                                    })
                            except Exception as e:
                                logger.warning(f"Failed to retrieve previous chunk for doc {doc_id}, chunk {chunk_index}: {str(e)}")

                        # Search for next chunk
                        if chunk_index < total_chunks - 1:
                            try:
                                next_results = self.collection.similarity_search_with_score(
                                    query="",
                                    k=1,
                                    filter={
                                        "$and": [
                                            {"original_doc_id": {"$eq": doc_id}},
                                            {"chunk_index": {"$eq": chunk_index + 1}}
                                        ]
                                    }
                                )
                                if next_results:
                                    surrounding_chunks.append({
                                        "text": next_results[0][0].page_content,
                                        "type": "next",
                                        "index": chunk_index + 1
                                    })
                            except Exception as e:
                                logger.warning(f"Failed to retrieve next chunk for doc {doc_id}, chunk {chunk_index}: {str(e)}")

                    chunk = {
                        "text": doc.page_content,
                        "metadata": metadata,
                        "score": score,
                        "surrounding_chunks": surrounding_chunks
                    }
                    retrieved_chunks.append(chunk)
                    
                    logger.debug(f"Retrieved chunk {chunk_index}/{total_chunks} from document {doc_id}")
            
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks with surrounding context for query: {query}")
            return retrieved_chunks
        
        except Exception as e:
            logger.error(f"Error retrieving chunks with document context: {str(e)}")
            return []

    def get_full_document_context(self, doc_id: str) -> List[Dict]:
        """Retrieve all chunks from a specific document in order."""
        try:
            initial_result = self.collection.similarity_search_with_score(
                query="",
                k=1,
                filter={"original_doc_id": {"$eq": doc_id}}
            )
            
            if not initial_result:
                return []
                
            total_chunks = initial_result[0][0].metadata.get('total_chunks')
            
            all_chunks = []
            for i in range(total_chunks):
                results = self.collection.similarity_search_with_score(
                    query="",
                    k=1,
                    filter={
                        "$and": [
                            {"original_doc_id": {"$eq": doc_id}},
                            {"chunk_index": {"$eq": i}}
                        ]
                    }
                )
                if results:
                    chunk = {
                        "text": results[0][0].page_content,
                        "metadata": results[0][0].metadata,
                        "index": i
                    }
                    all_chunks.append(chunk)
                    
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving full document context for doc_id '{doc_id}': {str(e)}")
            raise
