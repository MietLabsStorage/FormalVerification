from dataclasses import dataclass
from collections.abc import Sequence

@dataclass
class Hbm:
    blob: Sequence[bool] = [0] * 10