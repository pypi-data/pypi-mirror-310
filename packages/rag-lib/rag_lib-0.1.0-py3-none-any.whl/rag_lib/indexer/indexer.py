from typing import List, Dict
import json
import os

class Indexer:
    def __init__(self, index_dir='indexes'):
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)

    def index(self, chunks: List[str], metadata: Dict[str, str]) -> None:
        filename = metadata.get('filename', 'unknown')
        index_file = os.path.join(self.index_dir, f'{filename}.json')
        with open(index_file, 'w') as f:
            json.dump({'chunks': chunks, 'metadata': metadata}, f)
