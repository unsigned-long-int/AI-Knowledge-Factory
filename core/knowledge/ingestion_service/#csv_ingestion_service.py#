import pandas as pd

from pathlib import Path
from dataclasses import dataclass


@dataclass
class CSVIngestionService:
    csv_path: Path

    def ingest(self, embeddings: pd.DataFrame) -> None:
        embeddings.to_csv(self.csv_path, index=False)
