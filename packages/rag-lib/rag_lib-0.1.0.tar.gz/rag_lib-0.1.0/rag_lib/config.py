from pydantic_settings import BaseSettings
from typing import Optional
import yaml

class LLMConfig(BaseSettings):
    model_name: str
    api_base: str
    api_key: str
    system_prompt: str

class EmbeddingModelConfig(BaseSettings):
    model_name: str

class RetrieverConfig(BaseSettings):
    documents_path: str

class AppConfig(BaseSettings):
    llm: LLMConfig
    embedding_model: EmbeddingModelConfig
    retriever: RetrieverConfig

    class Config:
        env_prefix = ''
        case_sensitive = False

def load_config(config_file_path: str = 'config/config.yaml') -> AppConfig:
    with open(config_file_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    return AppConfig(**config_dict)
