from dataclasses import dataclass
from typing import List

from infrastructure.metadata_generator import append_metadata


@append_metadata(description='responsible for collecting articles about internal company news')
@dataclass(frozen=True)
class CollectorMicrosite:
    endpoint: str

    def collect_knowledge_stream(self) -> List[str]:
        pass
