from typing import Dict, Optional, Type

from core.knowledge.collection_service import (
    CollectorProtocol,
    CollectorMicrosite,
    CollectorPatch
)

from .exceptions import InvalidCollector, NonRegisteredCollector


class CollectorRegistryMeta(type):
    _registry: Dict[str, Type[CollectorProtocol]] = {}

    def __getitem__(cls, key: str) -> Optional[Type[CollectorProtocol]]:
        if key not in cls._registry:
            message = f'collector key: {key} is not found in _registry'
            raise NonRegisteredCollector('collector key')
        return cls._registry.get(key)

    def __repr__(cls) -> str:
        return ' | '.join(f'collector_key={name},'
                          f'implementation={getattr(collector, "metadata", "unknown")}'
                          for name, collector in cls._registry.items())

    def register(
            cls,
            key: str,
            collector_class: Type[CollectorProtocol]
    ) -> None:
        if not hasattr(collector_class, 'metadata'):
            error_message = '{!r} does not have ClassVar[str] = metadata'.format(
                collector_class
            )
            raise InvalidCollector(error_message)

        cls._registry[key] = collector_class


class CollectorRegistry(metaclass=CollectorRegistryMeta):
    pass


def update_collector_registry() -> None:
    CollectorRegistry.register('microsite', CollectorMicrosite)
    CollectorRegistry.register('patch', CollectorPatch)
