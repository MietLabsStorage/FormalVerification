from dataclasses import dataclass
import random
from typing import List

import deal

from hbm import Hbm

@dataclass
class HbmWorkload:
    workload: int # 0 - write, 1 - read, 2, 3 - free,
    ticks: int # when 0 then free
    task_id: int

@dataclass
class Task:
    task_id: int
    start_addr: int
    end_addr: int
    part: int
    parts_count: int
    part_idx: int
    task_group_id: int
    tpc_id: int
    op: int # 1 - write, 2 - read
    blob: List[int]
    canGet: int

class Vm:
    def __init__(self, hbm: Hbm):
        self.__hbm = hbm
        self.__workloadTable = HbmWorkload(2, 0, 0)
        for i, cell in enumerate(hbm.blob):
            self.__workloadTable[i] = {}
        self.__taskQueue: List[Task] = []
        @property
        def nextId(self):
            return 0 if len(self.__taskQueue) == 0 else self.__taskQueue[-1].task_id + 1

    def tick(self):
        for task in filter(lambda x: x.canGet == 1 and x.part_idx == 1, self.__taskQueue):
            isFree = True
            for i in range(task.start_addr, task.end_addr + 1):
                #!!!тут сложнее, перепроверь
                isFree = isFree and self.__workloadTable[i].workload != 0 and self.__workloadTable[i].workload != 1
            if isFree:
                for i in range(task.start_addr, task.end_addr + 1):
                    self.__workloadTable[i].workload = task.op
                    self.__workloadTable[i].ticks = random.randint(10,30)
                    self.__workloadTable[i].task_id = task.task_id

    def read(self, start_addr, end_addr, part, parts_count, task_group_id, tcp_id):
        self.__taskQueue.append(Task(self.nextId, start_addr, end_addr, part, parts_count, part, task_group_id, tcp_id, 1, []))
    
    @deal.pre(lambda start_addr: start_addr >= 0)
    @deal.pre(lambda start_addr: start_addr < 10)
    @deal.pre(lambda end_addr: end_addr >= 0)
    @deal.pre(lambda end_addr: end_addr < 10)
    @deal.ensure(lambda start_addr, end_addr: start_addr > end_addr)
    @staticmethod
    def write(self: Vm, start_addr: int, end_addr: int, part: int, parts_count: int, task_group_id: int, tcp_id: int, blob: List[int]) -> None:
        self.__taskQueue.append(Task(self.nextId, start_addr, end_addr, part, parts_count, part, task_group_id, tcp_id, 0, blob))
        if part == parts_count:
            for task in self.__taskQueue:
                if task.task_group_id == task_group_id:
                    task.canGet = 1
    
    @deal.pre(lambda n: n >= 0)
    @staticmethod
    def qq(n: int, start_addr: int, end_addr: int, part: int, parts_count: int, task_group_id: int, tcp_id: int, blob: List[int]) -> None:
        pass