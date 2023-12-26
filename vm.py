from dataclasses import dataclass
import random
from typing import List, Self
import deal
from main import m_hbm
from main import Tpc

  
__workloadTable = []
for i, cell in enumerate(m_hbm.blob):
    __workloadTable[i] = [2, 0, 0]
__taskQueue = []
__tcp = []
for i in range(0, 6):
    __tcp.append(Tpc(i, 0))


@deal.pre(lambda taskQueue: len(taskQueue) >= 0)
@deal.post(lambda result: result >= 0)
def nextId(taskQueue: List[List[int]]) -> int:
    if len(taskQueue) == 0:
        return 0
    else:
        return taskQueue[len(taskQueue) - 1][0] + 1


def tick(workloadTable: List[List[int]], taskQueues: List[List[int]]) -> None:
    filtered_tasks = []
    for task in taskQueues:
        if(task[8] == 1 and task[5] == 1):
            filtered_tasks.append(task)
    for task in filtered_tasks:
        if task[11] == 0:   
            isFree = True
            for i in range(task[1], task[2] + 1):
                #если память читается а мы хотим записать добавить проверку
                if workloadTable[i][0] == 0:
                    isFree = False
                    break
                        
            if isFree:
                ticktack = random.randint(10,30)
                for i in range(task[1], task[2] + 1):
                    workloadTable[i][0] = task[8]
                    workloadTable[i][1] = ticktack
                    workloadTable[i][2] = task[0]  
                task[11] = 1              
                
        elif task[11] == 1:
            if task[10] == 0:
                if task[8] == 0:
                    for i in range(task[1], task[2] + 1):
                        workloadTable[i][0] -= 1          
                        if workloadTable[i][1] == 0:
                            #в нулевой тик завершить операцию
                            workloadTable[i][0] == 2
                            task[11] = 2

                else:
                    read()
                    for i in range(task[1], task[2] + 1):
                        workloadTable[i][0] -= 1          
                        if workloadTable[i][1] == 0:
                             #в нулевой тик завершить операцию
                            workloadTable[i][0] == 2
                            task[11] = 2
                
        #избавляемся от выполненных задач
        condition = lambda x: x[11] == 2
        taskQueue = [x for x in taskQueue if not condition(x)]



@deal.pre(lambda start_addr: start_addr >= 0)
@deal.pre(lambda start_addr: start_addr < 100)
@deal.pre(lambda end_addr: end_addr >= 0)
@deal.pre(lambda end_addr: end_addr < 100)
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
    a = 0
    for i in range (n):
        a += 1