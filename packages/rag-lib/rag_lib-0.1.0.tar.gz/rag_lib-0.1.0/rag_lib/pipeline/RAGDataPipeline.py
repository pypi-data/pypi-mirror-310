from lib.converter.converter import Converter
from lib.clearer.clearer import Clearer
from lib.chunker.chunker import Chunker
from lib.indexer.indexer import Indexer

class RAGDataPipeline:
    def __init__(self):
        self.converter = Converter()
        self.clearer = Clearer()
        self.chunker = Chunker()
        self.indexer = Indexer()

    def process_document(self, file_path: str):
        converted = self.converter.convert(file_path)
        cleaned_text = self.clearer.clean(converted['text'])
        chunks = self.chunker.chunk(cleaned_text)
        self.indexer.index(chunks, converted['metadata'])
        return f'Document processed and indexed: {file_path}'
