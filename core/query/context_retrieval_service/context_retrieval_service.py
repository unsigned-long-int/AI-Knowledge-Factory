import pandas as pd

from typing import List
from dataclasses import dataclass, field

from core.knowledge.retrieval_service import RetrievalServiceProtocol
from infrastructure.cosine_similarity import cosine_similarity


@dataclass
class ContextRetrievalService:
    retrieval_service: RetrievalServiceProtocol
    knowledge_embeddings: pd.DataFrame = field(
        default_factory=pd.DataFrame,
        init=False,
        repr=False
    )

    def __post_init__(self) -> None:
        self.knowledge_embeddings = self.retrieval_service.retrieve_embeddings()

    def retrieve_context_matrix(self, query_embedding: List[float], context_size: int) -> pd.DataFrame:
        context_cosine_matrix = [
            (row['context'], cosine_similarity(
                query_embedding=query_embedding,
                knowledge_embedding=row['embedding']))
            for i, row in self.knowledge_embeddings.iterrows()
        ]

        context_cosine_matrix.sort(
            key=lambda similarity: similarity[1],
            reverse=True
        )
        return context_cosine_matrix[:context_size]
