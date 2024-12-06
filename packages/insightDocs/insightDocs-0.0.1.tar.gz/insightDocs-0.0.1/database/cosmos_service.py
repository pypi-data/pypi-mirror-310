from typing import Generator, List, Dict, Optional, Any
import logging
import tiktoken
from pymongo import MongoClient
from llama_index.vector_stores.azurecosmosmongo import AzureCosmosDBMongoDBVectorSearch
from llama_index.core import Document as LlamaDocument
from llama_index.core import StorageContext, VectorStoreIndex
from tqdm.auto import tqdm

from config.models import DocumentChunk

logger = logging.getLogger(__name__)

class CosmosDBService:
    def __init__(
        self,
        connection_string: str,
        db_name: str,
        collection_name: str,
        embedding_model_name: str = "BAAI/bge-base-en-v1.5",
        max_tokens: int = 7000,
        search_params: Dict = None
    ):
        self.connection_string = connection_string
        self.db_name = db_name
        self.collection_name = collection_name
        self._client = None
        self._vector_store = None
        self._index = None
        self._initialized = False
        
        self.tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")
        self.max_tokens = max_tokens
        
        self.search_params = search_params or {
            "ef_construction": 400,
            "ef_search": 200,
            "m": 128,
            "metric": "cosine"
        }
        
       
    @property
    def client(self):
        if self._client is None:
            self._client = MongoClient(self.connection_string)
            logger.info(f"Successfully connected to MongoDB client for database: {self.db_name}")
        return self._client
    
    @property
    def vector_store(self):
        if self._vector_store is None:
            self._vector_store = AzureCosmosDBMongoDBVectorSearch(
                mongodb_client=self.client,
                db_name=self.db_name,
                collection_name=self.collection_name,
                index_params={
                    "maxVectorCount": 1000000,
                    "similarity": self.search_params["metric"],
                    "m": self.search_params["m"],
                    "efConstruction": self.search_params["ef_construction"],
                    "efSearch": self.search_params["ef_search"],
                    "vector": {
                        "similarity": self.search_params["metric"]
                    }
                }
            )
        return self._vector_store

    async def _load_existing_index(self) -> None:
        """Load existing index from vector store if documents exist."""
        try:
            collection = self.client[self.db_name][self.collection_name]
            doc_count = collection.count_documents({})
            
            if doc_count > 0:
                logger.info(f"Found {doc_count} existing documents. Loading index...")
                storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
                self._index = VectorStoreIndex.from_vector_store(
                    vector_store=self.vector_store,
                    storage_context=storage_context
                )
                self._initialized = True
                logger.info("Successfully loaded existing index")
            else:
                logger.info("No existing documents found in collection")
                self._initialized = False
                
        except Exception as e:
            logger.error(f"Error loading existing index: {str(e)}")
            self._initialized = False
            raise

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using the ada tokenizer."""
        return len(self.tokenizer.encode(text))
    
    def _split_text_by_tokens(self, text: str, max_tokens: int = None) -> Generator[str, None, None]:
        """Split text into chunks that don't exceed max_tokens."""
        max_tokens = max_tokens or self.max_tokens
        tokens = self.tokenizer.encode(text)
        
        chunks = []
        current_chunk: List[int] = []
        current_size = 0
        
        for token in tokens:
            current_chunk.append(token)
            current_size += 1
            
            if current_size >= max_tokens:
                chunk_text = self.tokenizer.decode(current_chunk)
                yield chunk_text
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            yield self.tokenizer.decode(current_chunk)

    def _convert_to_llama_documents(self, chunks: List[DocumentChunk], batch_size: int = 100) -> Generator[List[LlamaDocument], None, None]:
        """Convert DocumentChunk objects to LlamaIndex Documents with batching and token management."""
        current_batch = []
        
        for chunk in chunks:
            if self._count_tokens(chunk.text) > self.max_tokens:
               
                for idx, subtext in enumerate(self._split_text_by_tokens(chunk.text)):
                    doc = self._create_llama_document(chunk, subtext, is_split=True, split_idx=idx)
                    current_batch.append(doc)
                    
                    if len(current_batch) >= batch_size:
                        yield current_batch
                        current_batch = []
            else:
                # Process normal chunk
                doc = self._create_llama_document(chunk, chunk.text)
                current_batch.append(doc)
                
                if len(current_batch) >= batch_size:
                    yield current_batch
                    current_batch = []
        
        if current_batch:
            yield current_batch

    def _create_llama_document(self, chunk: DocumentChunk, text: str, is_split: bool = False, split_idx: int = None) -> LlamaDocument:
        """Helper method to create a LlamaDocument with proper metadata."""
        chunk_id = f"{str(chunk.id)}_split_{split_idx}" if is_split else str(chunk.id)
        
        base_metadata = {
            "chunk_id": chunk_id,
            "original_doc_id": str(chunk.original_doc_id),
            "filepath": str(chunk.filepath),
            "chunk_index": int(chunk.chunk_index),
            "total_chunks": int(chunk.total_chunks),
            "is_split": is_split
        }
        
        if is_split:
            base_metadata.update({
                "original_chunk_id": str(chunk.id),
                "split_index": split_idx
            })
        
        # Add flattened metadata
        additional_metadata = {}
        if chunk.metadata:
            additional_metadata = self._flatten_metadata(chunk.metadata)
        
        if chunk.window_metadata:
            window_metadata = self._flatten_metadata(
                {"window": chunk.window_metadata}, 
                parent_key="window"
            )
            additional_metadata.update(window_metadata)
        
        metadata = {**base_metadata, **additional_metadata}
        
        return LlamaDocument(
            text=text,
            metadata=metadata,
            id_=chunk_id
        )

    async def store_chunks(self, chunks: List[DocumentChunk], batch_size: int = 100) -> None:
        """Store document chunks with batching and progress tracking."""
        try:
            logger.info(f"Starting to process {len(chunks)} chunks")
            doc_generator = self._convert_to_llama_documents(chunks, batch_size)
            
            storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            total_processed = 0
            
            with tqdm(total=len(chunks), desc="Processing documents") as pbar:
                for batch in doc_generator:
                    if not self._initialized:
                        self._index = VectorStoreIndex.from_documents(
                            documents=batch,
                            storage_context=storage_context
                        )
                        self._initialized = True
                    else:
                        self._index.insert_nodes(batch)
                    
                    total_processed += len(batch)
                    pbar.update(len(batch))
                    logger.debug(f"Processed batch: {total_processed}/{len(chunks)}")
            
            logger.info(f"Successfully completed storing {total_processed} documents")
            
        except Exception as e:
            logger.error(f"Error in store_chunks: {str(e)}")
            raise

    async def retrieve_chunks(
        self, 
        query: str, 
        top_k: int = 5, 
        similarity_threshold: float = 0.5,
        rerank: bool = True
    ) -> List[Dict]:
        """Enhanced retrieval with filtering, reranking and split handling."""
        try:
            if not self._initialized:
                await self._load_existing_index()
                
            if not self._initialized:
                logger.warning("No documents have been indexed yet")
                return []

            query_engine = self._index.as_query_engine(
                similarity_top_k=min(top_k * 2, 100) if rerank else top_k,
                response_mode="no_text",
                vector_store_kwargs={
                    "search_params": {
                        "ef": self.search_params["ef_search"],
                        "metric": self.search_params["metric"]
                    }
                }
            )
            
            response = query_engine.query(query)
            
            chunk_groups = {}
            filtered_chunks = []
            
            for node in response.source_nodes:
                has_score = hasattr(node, 'score')
                score_value = node.score if has_score else None
                logger.debug(f"Has score: {has_score}, Score value: {score_value}, Threshold: {similarity_threshold}")
                
                if not has_score or score_value < similarity_threshold:
                    logger.info(f"Skipping node due to score requirements")
                    continue
                
                
                chunk = {
                    "text": node.node.text,
                    "metadata": node.node.metadata,
                    "score": node.score,
                    "id": node.node.id_
                }
                
                if chunk["metadata"].get("is_split", False):
                    original_id = chunk["metadata"]["original_chunk_id"]
                    if original_id not in chunk_groups:
                        chunk_groups[original_id] = []
                    chunk_groups[original_id].append(chunk)
                else:
                    filtered_chunks.append(chunk)
            
            for original_id, splits in chunk_groups.items():
                combined_text = " ".join(c["text"] for c in sorted(
                    splits,
                    key=lambda x: x["metadata"]["split_index"]
                ))
                
                base_metadata = splits[0]["metadata"].copy()
                base_metadata.pop("is_split", None)
                base_metadata.pop("split_index", None)
                
                combined_chunk = {
                    "text": combined_text,
                    "metadata": base_metadata,
                    "score": max(c["score"] for c in splits),
                    "id": original_id
                }
                filtered_chunks.append(combined_chunk)
            
            filtered_chunks.sort(key=lambda x: x["score"], reverse=True)
            final_chunks = filtered_chunks[:top_k]
            
            logger.info(f"Retrieved {len(final_chunks)} chunks for query: {query}")
            return final_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving chunks: {str(e)}")
            return []

    def _matches_filter(self, metadata: Dict, filter_dict: Dict) -> bool:
        """Helper method to check if metadata matches filter criteria."""
        for key, value in filter_dict.items():
            if key not in metadata:
                return False
            if isinstance(value, (list, tuple)):
                if metadata[key] not in value:
                    return False
            elif metadata[key] != value:
                return False
        return True

    async def initialize_vector_store(self) -> None:
        """Initialize and validate the vector store."""
        try:
            logger.info("Initializing vector store...")
            _ = self.vector_store
            
            await self._load_existing_index()
            
            if self._validate_vector_store():
                logger.info("Vector store initialized and validated successfully")
            else:
                logger.error("Vector store validation failed")
                raise Exception("Vector store validation failed")
                
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise

    def _validate_vector_store(self) -> bool:
        """Validate that the vector store is properly initialized."""
        try:
            collection = self.client[self.db_name][self.collection_name]
            stats = collection.stats()
            logger.info(f"Vector store validation successful. Collection stats: {stats}")
            return True
        except Exception as e:
            logger.error(f"Vector store validation failed: {str(e)}")
            return False


    def _flatten_metadata(self, metadata: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """Flatten nested metadata dictionary."""
        items: List = []
        for key, value in metadata.items():
            new_key = f"{parent_key}_{key}" if parent_key else key

            if value is None:
                items.append((new_key, None))
            elif isinstance(value, (str, int, float)):
                items.append((new_key, value))
            elif isinstance(value, dict):
                items.extend(self._flatten_metadata(value, new_key).items())
            elif isinstance(value, list):
                items.append((new_key, str(value)))
            else:
                items.append((new_key, str(value)))

        return dict(items)