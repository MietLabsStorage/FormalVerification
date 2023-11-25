from typing import Sequence
import deal

@deal.post(lambda result: result >= 0)
def count(items: Sequence[str], item: str) -> int:
    return -1

@deal.post(lambda result: result >= 0)
@deal.pre(lambda nm: nm >= 4)
def numb(nm: int) -> int:
    return nm * nm - 10