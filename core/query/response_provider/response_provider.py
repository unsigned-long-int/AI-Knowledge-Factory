import pandas as pd

from dataclasses import dataclass
from openai import OpenAI
from typing import Dict, List, Any


from infrastructure.embedding_generation_service import EmbeddingGenerator
from core.query.context_retrieval_service import ContextRetrievalService

from .exceptions import ResponseProviderError


@dataclass
class ResponseProvider:
    client: OpenAI
    context_retrieval_service: ContextRetrievalService

    def provide_response(self, query: str, context_size: int) -> Dict[str, Any]:
        messages = self._generate_messages(query, context_size)

        try:
            response = self.client.chat.completions.create(
                model='gpt-4o',
                messages=messages
            )

            return response
        except Exception as e:
            raise ResponseProviderError from e

    def _generate_messages(self, query: str, context_size: int) -> List[Dict[str, str]]:
        embeddings_generator = EmbeddingGenerator(
            client=self.client,
            datastream=query
        )

        query_embedding = embeddings_generator.generate_embedding()
        context_matrix = self.context_retrieval_service.retrieve_context_matrix(
            query_embedding=query_embedding,
            context_size=context_size
        )
        developer_context = (f'Using below context, provide most precise and fact-based response to the user question.'
                             f'Context: {"\n".join(context for context, _ in context_matrix)}')
        user_context = f'Question: {query}'

        messages = [
            {"role": "developer", "content": developer_context},
            {"role": "user", "content": user_context}
        ]
        return messages
