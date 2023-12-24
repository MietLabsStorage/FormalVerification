from dataclasses import dataclass
import random
from typing import List, Self
import deal
from main import m_hbm

  
__workloadTable = []
for i, cell in enumerate(m_hbm.blob):
    __workloadTable[i] = [2, 0, 0]
__taskQueue = []


@deal.pre(lambda taskQueue: len(taskQueue) >= 0)
@deal.post(lambda result: result >= 0)
def nextId(taskQueue: List[List[int]]) -> int:
    if len(taskQueue) == 0:
        return 0
    else:
        return taskQueue[len(taskQueue) - 1][0] + 1


def tick(workloadTable: List[List[int], taskQueues: List[List[int]]]):
    for task in filter(lambda x: x.canGet == 1 and x.part_idx == 1, __taskQueue):
        isFree = True
        for i in range(task.start_addr, task.end_addr + 1):
            # проверка каждой яячейко на то что с ней сейчас можно работать
            #!!!тут сложнее логика должна быть 
            isFree = isFree and __workloadTable[i].workload != 0 and __workloadTable[i].workload != 1
        if isFree:
            ticktack = random.randint(10,30)
            for i in range(task.start_addr, task.end_addr + 1):
                workloadTable[i][0] = task.op
                workloadTable[i][1] = ticktack
                workloadTable[i][2] = task.task_id                
        # !!! если workloadTable[i][1] = 0 то нужно 
        #       если таска была на запись - записать в hbm
        #       если таска была на чтение - то записать из hbm в task[9]


@deal.pre(lambda start_addr: start_addr >= 0)
@deal.pre(lambda start_addr: start_addr < 10)
@deal.pre(lambda end_addr: end_addr >= 0)
@deal.pre(lambda end_addr: end_addr < 10)
@deal.pre(lambda start_addr, end_addr: start_addr > end_addr)
def read(
    taskQueue: list[list[int]],
    start_addr: int,
    end_addr: int,
    part: int,
    parts_count: int,
    task_group_id: int,
    tcp_id: int
) -> None:
    taskQueue.append([nextId(taskQueue), start_addr, end_addr, part, parts_count, part, task_group_id, tcp_id, 1, [], 0])
    # если пришел последний пакет из группы
    if part == parts_count:
        # то для всех таск
        for i in range(len(taskQueue)):
            # из этой группы
            if taskQueue[i][6] == task_group_id:
                # разрешаем таски на взятие в работу
                taskQueue[i][10] = 1


@deal.pre(lambda start_addr: start_addr >= 0)
@deal.pre(lambda start_addr: start_addr < 100)
@deal.pre(lambda end_addr: end_addr >= 0)
@deal.pre(lambda end_addr: end_addr < 100)
@deal.pre(lambda start_addr, end_addr: start_addr > end_addr)
def write(
    taskQueue: list[list[int]],
    start_addr: int,
    end_addr: int,
    part: int,
    parts_count: int,
    task_group_id: int,
    tcp_id: int,
    blob: List[int]
) -> None:
    taskQueue.append([nextId(taskQueue), start_addr, end_addr, part, parts_count, part, task_group_id, tcp_id, 0, blob, 0])
    # если пришел последний пакет из группы
    if part == parts_count:
        # то для всех таск
        for i in range(len(taskQueue)):
            # из этой группы
            if taskQueue[i][6] == task_group_id:
                # разрешаем таски на взятие в работу
                taskQueue[i][10] = 1


@deal.pre(lambda n: n >= 0)
@deal.post(lambda n: n > 0)
def deal_test(n: int) -> None:
    return n - 3