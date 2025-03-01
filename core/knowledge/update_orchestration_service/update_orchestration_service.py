import pandas as pd
from dataclasses import dataclass
from openai import OpenAI

from infrastructure.embedding_generation_service import EmbeddingGenerator
from core.knowledge.collection_service import CollectorProtocol
from core.knowledge.ingestion_service import IngestionServiceProtocol
from .exceptions import MissingDatastream


@dataclass
class UpdateOrchestrationService:
    client: OpenAI
    collector: CollectorProtocol
    ingestor: IngestionServiceProtocol

    def run_pipeline(self) -> None:
        datastream = self.collector.collect_knowledge_stream()
        if not datastream:
            raise MissingDatastream(
                f'no datastream is found for: {repr(self)}'
            )

        embeddings = []
        for record in datastream:
            embedding_generator = EmbeddingGenerator(
                client=self.client,
                datastream=record
            )
            embedding = embedding_generator.generate_embedding()
            embeddings.append({
                'context': record,
                'embedding': embedding
            })
        self.ingestor.ingest(pd.DataFrame(embeddings))
