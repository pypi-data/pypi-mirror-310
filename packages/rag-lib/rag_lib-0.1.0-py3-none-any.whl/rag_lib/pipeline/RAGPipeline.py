from typing import Optional, Dict, Any
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.langchain import LangchainEmbedding
from lib.retriever.retriever import Retriever
from lib.prompt.prompt_augmentation import PromptAugmentation
from lib.answer_generation.answer_generation import AnswerGeneration
from lib.config import AppConfig

class RAGPipeline:
    def __init__(
        self,
        config: AppConfig,
        llm: OpenAILike = None,
        embed_model: Optional[LangchainEmbedding] = None,
        retriever: Optional[Retriever] = None
    ):
        self.config = config
        if retriever:
            self.retriever = retriever
        else:
            if not embed_model:
                raise ValueError("An embed_model must be provided if retriever is not provided")
            self.retriever = Retriever(config.retriever, embed_model)
        
        self.prompt_augmentation = PromptAugmentation()
        if not llm:
            raise ValueError("An llm must be provided")
        self.answer_generation = AnswerGeneration(llm)
    
    def query(
        self,
        question: str,
        prompt_template: Optional[str] = None,
        additional_info: Optional[str] = None,
        technical_fields: Optional[Dict[str, Any]] = None
    ) -> str:
        # Adding additional info to index
        if additional_info:
            self.retriever.add_document(additional_info)
        
        # Logging technical fields
        if technical_fields:
            print(f"Technical fields: {technical_fields}")
        
        # Updating prompt template if provided
        if prompt_template:
            self.prompt_augmentation.template = prompt_template
        
        # Getting context and generating answer
        context = self.retriever.retrieve(question)
        prompt = self.prompt_augmentation.construct_prompt(context, question)
        answer = self.answer_generation.generate_answer(prompt)
        return answer
