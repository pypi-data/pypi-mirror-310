from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from lib.config import RetrieverConfig
from llama_index.embeddings.langchain import LangchainEmbedding

class Retriever:
    def __init__(self, retriever_config: RetrieverConfig, embed_model: LangchainEmbedding, chunk_size: int = 1024):
        self.documents = SimpleDirectoryReader(retriever_config.documents_path, recursive=True).load_data()
        self.index = VectorStoreIndex.from_documents(
            self.documents,
            embed_model=embed_model,
            chunk_size=chunk_size
        )
        self.embed_model = embed_model
    
    def add_document(self, document_text: str):
        new_doc = Document(text=document_text)
        self.index.insert(new_doc)
    
    def retrieve(self, question: str) -> str:
        retriever = self.index.as_retriever()
        retrieved_docs = retriever.retrieve(question)
        context = "\n\n".join([doc.text for doc in retrieved_docs])
        return context
