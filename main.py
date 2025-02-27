from openai import OpenAI
from pathlib import Path

from infrastructure.credentials_loader import load_credentials
from infrastructure.manifest_loader import load_manifest
from infrastructure.ui_interface.cli import CLIParser
from infrastructure.event_orchestration_service.event_orchestrator import EventOrchestrator

from core.knowledge.retrieval_service import CSVRetrievalService
from core.knowledge.ingestion_service import CSVIngestionService
from core.knowledge.ai_knowledge_factory_service import AIKnowledgeFactory


def main() -> None:
    event_orchestrator = EventOrchestrator()
    api_key = load_credentials(event_orchestrator)
    manifest = load_manifest(event_orchestrator)

    client = OpenAI(api_key=api_key)

    ingestor = CSVIngestionService(csv_path='./repositories/base.csv')
    retriever = CSVRetrievalService(
        csv_path=Path('./repositories/base.csv')
    )

    ai_knowledge_factory = AIKnowledgeFactory(
        client=client,
        ingestor=ingestor,
        retriever=retriever
    )

    cli_parser = CLIParser(
        ai_knowledge_factory=ai_knowledge_factory,
        prog_name=manifest.prog_name,
        description=manifest.description,
        default_context_size=manifest.default_context_size
    )

    print(cli_parser.process_query())

    if event_orchestrator.queue:
        handle_event(event_orchestrator.queue.pop(0))


if __name__ == '__main__':
    main()
