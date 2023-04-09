 #By:
 	# Anuja Patil , Neethu Duggi , Vishwa Patel , Apurva Ratnaparkhi

from typing import List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from assets.Vectors import Vector2

@dataclass
class SavedState:
    score: int
    hearts: int
    targetNumZombies: float
    playerPosition: "Vector2"
    zombiePositions: List["Vector2"]
    zombieHearts: List[int]
    controls: List[str]
