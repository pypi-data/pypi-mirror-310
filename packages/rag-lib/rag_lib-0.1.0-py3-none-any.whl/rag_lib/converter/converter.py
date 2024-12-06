import os
from typing import Dict
import PyPDF2
import docx2txt
import csv

class Converter:
    def __init__(self, supported_formats=None):
        self.supported_formats = supported_formats or ['pdf', 'docx', 'csv']

    def convert(self, file_path: str) -> Dict[str, str]:
        file_extension = os.path.splitext(file_path)[-1].lower().lstrip('.')
        if file_extension not in self.supported_formats:
            raise ValueError(f'Unsupported file format: {file_extension}')

        if file_extension == 'pdf':
            text = self._convert_pdf(file_path)
        elif file_extension == 'docx':
            text = self._convert_docx(file_path)
        elif file_extension == 'csv':
            text = self._convert_csv(file_path)
        else:
            text = ''

        return {
            'text': text,
            'metadata': {'filename': os.path.basename(file_path)}
        }

    def _convert_pdf(self, file_path: str) -> str:
        text = ''
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _convert_docx(self, file_path: str) -> str:
        text = docx2txt.process(file_path)
        return text

    def _convert_csv(self, file_path: str) -> str:
        text = ''
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                text += ' '.join(row) + '\n'
        return text
