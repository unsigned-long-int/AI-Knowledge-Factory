import pandas as pd

from dataclasses import dataclass, field
from typing import Optional, List
from openai import OpenAI


@dataclass
class EmbeddingGenerator:
    client: OpenAI
    datastream: str
    model: Optional[str] = field(default='text-embedding-3-small')

    def generate_embedding(self) -> List[float]:
        response = self.client.embeddings.create(
            input=self.datastream,
            model=self.model
        )
        return response.data[0].embedding
