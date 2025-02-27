import json
from dataclasses import dataclass
from openai import OpenAI
from typing import Dict, Any

from core.knowledge.collection_service import CollectorProtocol
from core.knowledge.ingestion_service import IngestionServiceProtocol
from core.knowledge.update_orchestration_service import UpdateOrchestrationService
from core.knowledge.retrieval_service import RetrievalServiceProtocol
from core.query.context_retrieval_service import ContextRetrievalService
from core.query.response_provider import ResponseProvider

from .collector_registry import CollectorRegistry, update_collector_registry
from .collector_dispatcher import dispatch_collector


@dataclass
class AIKnowledgeFactory:
    client: OpenAI
    ingestor: IngestionServiceProtocol
    retriever: RetrievalServiceProtocol

    def provide_response(self, query: str, context_size: int) -> Dict[str, Any]:
        self._update_knowledge_base(query)
        return self._fetch_response(
            query=query,
            context_size=context_size
        )

    def _update_knowledge_base(self, query: str) -> None:
        update_collector_registry()
        tools = [{'type': 'function',
                  'function': {
                      'name': 'dispatch_collector',
                      'description': dispatch_collector.__doc__,
                      'parameters': {
                          'type': 'object',
                          'properties': {
                              'collector_key': {
                                  'type': 'string',
                                  'description': f'{repr(CollectorRegistry)}'
                              }
                          },
                          'required': [
                              'collector_key'
                          ],
                          'additionalProperties': False
                      },
                      'strict': True
                  }
                  }
                 ]
        request = self.client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': query}],
            tools=tools
        )
        tool_call = request.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        collector_pointer = dispatch_collector(args['collector_key'])

        if collector_pointer:
            collector = collector_pointer('')
            self._orchestrate_knowledge_update(collector)

    def _orchestrate_knowledge_update(self, collector: CollectorProtocol) -> None:
        update_orchestration_service = UpdateOrchestrationService(
            client=self.client,
            collector=collector,
            ingestor=self.ingestor

        )
        update_orchestration_service.run_pipeline()

    def _fetch_response(self, query: str, context_size: int) -> Dict[str, Any]:
        context_retriever = ContextRetrievalService(
            retrieval_service=self.retriever
        )
        response_provider = ResponseProvider(
            client=self.client,
            context_retrieval_service=context_retriever
        )

        return response_provider.provide_response(
            query=query,
            context_size=context_size
        )
