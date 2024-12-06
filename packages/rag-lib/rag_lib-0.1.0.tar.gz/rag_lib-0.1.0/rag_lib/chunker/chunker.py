from typing import List

class Chunker:
    def chunk(self, text: str, chunk_size: int = 512, overlap: int = 0) -> List[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks
