# файл для проверки того что верификация с помощью библиотеки deal вообщше возможна

from typing import Sequence
import deal

@deal.post(lambda result: result >= 0)
def count(items: Sequence[str], item: str) -> int:
    return -1

@deal.post(lambda result: result >= 0)
@deal.pre(lambda nm: nm >= 4)
def numb(nm: int) -> int:
    return nm * nm - 10

deal.pre(lambda n: n > 0 and n < 10)
@deal.post(lambda result: result == 0)
def loop(n: int) -> int:
    s = 0
    for i in range(n):
        s = s + 1
    return s - n
