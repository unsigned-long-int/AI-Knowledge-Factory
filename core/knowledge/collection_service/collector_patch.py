from dataclasses import dataclass
from typing import List

from infrastructure.metadata_generator import append_metadata

MOCK_LIST = ['''Rick and Morty is an American adult animated science fiction sitcom created by Justin Roiland and Dan Harmon for Cartoon Network's nighttime programming block Adult Swim. The series follows the misadventures of Rick Sanchez, a cynical mad scientist, and his good-hearted but fretful grandson Morty Smith, who split their time between domestic life and interdimensional adventures that take place across an infinite number of realities, often traveling to other planets and dimensions through portals and on Rick's flying saucer. The general concept of Rick and Morty relies on two conflicting scenarios: domestic family drama and a misanthropic grandfather dragging his grandson into hijinks.''',
             '''Gravity Falls is an American mystery comedy animated television series created by Alex Hirsch for Disney Channel and Disney XD. The series follows the adventures of Dipper Pines (Jason Ritter) and his twin sister Mabel (Kristen Schaal), who are sent to spend the summer with their great-uncle (or "Grunkle") Stan (Hirsch) in Gravity Falls, Oregon, a mysterious town full of paranormal incidents and supernatural creatures. The kids help Stan run the "Mystery Shack", the tourist trap that he owns, while also investigating the local mysteries.''']


@append_metadata(description='contains the information about Rick & Morty and Gravity Falls Cartoons')
@dataclass
class CollectorPatch:
    endpoint: str

    def collect_knowledge_stream(self) -> List[str]:
        return MOCK_LIST
