import pandas as pd
import ast

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CSVRetrievalService:
    csv_path: Path

    def retrieve_embeddings(self) -> pd.DataFrame:
        knowledge_matrix = pd.read_csv(self.csv_path)
        knowledge_matrix['embedding'] = knowledge_matrix['embedding'].apply(
            ast.literal_eval
        )
        return knowledge_matrix
