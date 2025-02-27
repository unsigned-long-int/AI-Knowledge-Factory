from typing import Callable, TypeVar, Type

from core.knowledge.collection_service import CollectorProtocol

T = TypeVar('T', bound=CollectorProtocol)


def append_metadata(description: str) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        metadata = f'metadata: {description}'
        if (doc := cls.__doc__) is not None:
            metadata = f'{metadata},  __doc__: {doc}'
        cls.metadata = metadata
        return cls
    return decorator
