from typing import Optional

class PromptAugmentation:
    def __init__(self, template: Optional[str] = None):
        self.template = template or (
            "Given the context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Please provide a detailed answer to the question using the information from the context."
        )

    def construct_prompt(self, context: str, question: str) -> str:
        return self.template.format(context=context, question=question)
