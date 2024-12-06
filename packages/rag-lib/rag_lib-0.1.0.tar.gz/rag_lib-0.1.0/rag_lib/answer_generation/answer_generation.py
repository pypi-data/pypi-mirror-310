from llama_index.llms.openai_like import OpenAILike

class AnswerGeneration:
    def __init__(self, llm: OpenAILike):
        self.llm = llm

    def generate_answer(self, prompt: str) -> str:
        response = self.llm.complete(prompt)
        return response.strip()
