from typing import Optional, Type

from core.knowledge.collection_service import CollectorProtocol

from .collector_registry import CollectorRegistry


def dispatch_collector(collector_key: str) -> Optional[Type[CollectorProtocol]]:
    '''responsible for collecting information from different sources
    in order to enrich user's prompt with information from these sources'''
    return CollectorRegistry[collector_key]
