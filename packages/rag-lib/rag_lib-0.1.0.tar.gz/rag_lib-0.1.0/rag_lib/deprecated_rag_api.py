from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from llama_index import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.llms import OpenAI
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings import HuggingFaceEmbeddings

app = FastAPI()

# Определение моделей запросов и ответов
class QueryRequest(BaseModel):
    question: str
    prompt_template: Optional[str] = None
    additional_info: Optional[str] = None
    technical_fields: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str

# Определение системного промпта
system_prompt = (
    "You are a Q&A assistant. Your goal is to answer questions as accurately as possible "
    "based on the instructions and context provided."
)

# Инициализация LLM
llm = OpenAI(
    model_name="mistral-instruct-local-dir/",
    api_base="http://10.9.164.17:8951/v1",
    api_key="fake",
    system_prompt=system_prompt
)

# Инициализация модели эмбеддингов
embed_model = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name="/path/to/your/model")
)

# класс Retriever с возможностью добавления документов
class Retriever:
    def __init__(self, documents_path: str, embed_model: LangchainEmbedding, chunk_size: int = 1024):
        self.documents = SimpleDirectoryReader(documents_path).load_data()
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

# Класс для увеличения гибкости шаблона промпта
class PromptAugmentation:
    def __init__(self, template: Optional[str] = None):
        self.template = template or (
            "Given the context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Please provide a detailed answer to the question using the information from the context."
        )

    def construct_prompt(self, context: str, question: str) -> str:
        return self.template.format(context=context, question=question)

# Класс для генерации ответа
class AnswerGeneration:
    def __init__(self, llm: OpenAI):
        self.llm = llm

    def generate_answer(self, prompt: str) -> str:
        response = self.llm.complete(prompt)
        return response.strip()

class RAGPipeline:
    def __init__(
        self,
        documents_path: Optional[str] = None,
        llm: OpenAI = None,
        embed_model: Optional[LangchainEmbedding] = None,
        prompt_template: Optional[str] = None,
        retriever: Optional[Retriever] = None
    ):
        if retriever:
            self.retriever = retriever
        else:
            if not documents_path or not embed_model:
                raise ValueError("Обязательно должны быть переданы либо retriever, либо documents_path и embed_model")
            self.retriever = Retriever(documents_path, embed_model)
        
        self.prompt_augmentation = PromptAugmentation(prompt_template)
        self.answer_generation = AnswerGeneration(llm)
    
    def query(
        self,
        question: str,
        prompt_template: Optional[str] = None,
        additional_info: Optional[str] = None,
        technical_fields: Optional[Dict[str, Any]] = None
    ) -> str:
        # Добавление дополнительной информации в индекс
        if additional_info:
            self.retriever.add_document(additional_info)
        
        # Логирование технических полей
        if technical_fields:
            print(f"Technical fields: {technical_fields}")
        
        # Обновление шаблона промпта, если предоставлен
        if prompt_template:
            self.prompt_augmentation.template = prompt_template
        
        # Получение контекста и генерация ответа
        context = self.retriever.retrieve(question)
        prompt = self.prompt_augmentation.construct_prompt(context, question)
        answer = self.answer_generation.generate_answer(prompt)
        return answer

# Инициализация компонентов для API
documents_path = "/path/to/your/documents"
retriever = Retriever(documents_path, embed_model)
pipeline = RAGPipeline(
    llm=llm,
    embed_model=embed_model,
    retriever=retriever
)

# Эндпоинт для обработки запросов
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        answer = pipeline.query(
            question=request.question,
            prompt_template=request.prompt_template,
            additional_info=request.additional_info,
            technical_fields=request.technical_fields
        )
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))