from typing import Dict, List, Callable, Type

from infrastructure.event_orchestration_service.event_orchestrator.actions import (
    log_error,
    abort
)
from infrastructure.event_orchestration_service.events import events
from infrastructure.event_orchestration_service.event_orchestrator import EventOrchestrator


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.OpenAICredentialsLoadFailed: [log_error],
    events.OpenAIClientLoadFailed: [log_error],
    events.ManifestNotFound: [log_error],
    events.ManifestDecodingFailed: [log_error],
    events.MissingManifestItemsEncountered: [log_error],
    events.ManifestGenerationFailed: [log_error],
    events.AIFactoryFailedProvidingResponse: [log_error]
}


def handle_event(event: events.Event, event_orchestrator: EventOrchestrator) -> None:
    queue = [event]
    while queue:
        event = queue.pop(0)
        handlers = EVENT_HANDLERS[type(event)]

        for handler in handlers:
            handler(event=event, event_orchestrator=event_orchestrator)
            queue.extend(event_orchestrator.collect_new_events())
