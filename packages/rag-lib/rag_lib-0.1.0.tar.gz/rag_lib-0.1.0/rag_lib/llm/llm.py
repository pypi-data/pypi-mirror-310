from llama_index.llms.openai_like import OpenAILike
from lib.config import LLMConfig

def get_llm(llm_config: LLMConfig) -> OpenAILike:
    llm = OpenAILike(
        model_name=llm_config.model_name,
        api_base=llm_config.api_base,
        api_key=llm_config.api_key,
        system_prompt=llm_config.system_prompt
    )
    return llm
