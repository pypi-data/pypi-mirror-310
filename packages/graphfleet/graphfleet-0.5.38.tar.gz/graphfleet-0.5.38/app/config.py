from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import os

class LLMConfig(BaseModel):
    """Configuration for LLM settings."""
    api_key: str = Field(..., env="GRAPHRAG_API_KEY")
    model: str = Field(..., env="GRAPHRAG_LLM_MODEL")
    api_base: str = Field(..., env="GRAPHRAG_API_BASE")
    api_version: str = Field(..., env="GRAPHRAG_API_VERSION")
    max_tokens: int = Field(12000, env="GRAPHRAG_MAX_TOKENS")
    temperature: float = Field(0.0, env="GRAPHRAG_TEMPERATURE")

class EmbeddingConfig(BaseModel):
    """Configuration for embedding model settings."""
    model: str = Field(..., env="GRAPHRAG_EMBEDDING_MODEL")
    batch_size: int = Field(32, env="GRAPHRAG_EMBEDDING_BATCH_SIZE")

class GraphRAGConfig(BaseModel):
    """Configuration for GraphRAG-specific settings."""
    community_level: int = Field(2, env="GRAPHRAG_COMMUNITY_LEVEL")
    input_dir: str = Field(
        "graphfleet/output/20240828-113421/artifacts",
        env="GRAPHRAG_INPUT_DIR"
    )
    lancedb_uri: Optional[str] = None
    max_concurrent_requests: int = Field(32, env="GRAPHRAG_MAX_CONCURRENT")
    cache_embeddings: bool = Field(True, env="GRAPHRAG_CACHE_EMBEDDINGS")

class Settings(BaseSettings):
    """Main application settings."""
    # API settings
    api_title: str = "GraphFleet API"
    api_version: str = "0.5.35"
    api_description: str = "Advanced implementation of GraphRAG for enhanced LLM reasoning"
    debug: bool = Field(False, env="DEBUG")

    # CORS settings
    cors_origins: List[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )

    # GraphRAG settings
    llm: LLMConfig = LLMConfig()
    embedding: EmbeddingConfig = EmbeddingConfig()
    graphrag: GraphRAGConfig = GraphRAGConfig()

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.graphrag.lancedb_uri:
            self.graphrag.lancedb_uri = f"{self.graphrag.input_dir}/lancedb"

settings = Settings()