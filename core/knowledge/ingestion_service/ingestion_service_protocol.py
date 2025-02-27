import pandas as pd

from typing import Protocol, runtime_checkable


@runtime_checkable
class IngestionServiceProtocol(Protocol):
    def ingest(self, embeddings: pd.DataFrame) -> None:
        pass
