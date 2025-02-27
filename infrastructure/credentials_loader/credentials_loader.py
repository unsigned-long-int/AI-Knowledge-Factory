import os

from dotenv import load_dotenv
from typing import Optional

from infrastructure.event_orchestration_service.events import events
from infrastructure.event_orchestration_service.event_orchestrator import EventOrchestrator

load_dotenv()


def load_credentials(event_orchestrator: EventOrchestrator) -> Optional[str]:
    openai_creds: Optional[str] = os.getenv('OPENAI_API_KEY')

    if openai_creds is None:
        message = 'OPENAI_API_KEY is not found either in .env or environmental variable'
        event = events.OpenAICredentialsLoadFailed(message)
        event_orchestrator.queue.append(event)

    return openai_creds
