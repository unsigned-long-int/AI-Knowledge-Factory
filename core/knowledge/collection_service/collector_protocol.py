from typing import Protocol, runtime_checkable, List


@runtime_checkable
class CollectorProtocol(Protocol):
    endpoint: str

    def collect_knowledge_stream(self) -> List[str]:
        pass
