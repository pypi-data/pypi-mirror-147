from dataclasses import dataclass
from typing import Tuple


@dataclass
class MatchingResult:
    center: Tuple[int, int]
    rect: Tuple[Tuple[int, int], Tuple[int, int]]
    # for feature matching, the confidence will always be -1
    confidence: float
