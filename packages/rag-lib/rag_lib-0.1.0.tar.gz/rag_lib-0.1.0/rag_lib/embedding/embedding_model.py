from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings
from lib.config import EmbeddingModelConfig

def get_embedding_model(embedding_config: EmbeddingModelConfig) -> LangchainEmbedding:
    embed_model = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name=embedding_config.model_name)
    )
    return embed_model
