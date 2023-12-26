from typing import List
from attr import dataclass
from hbm import Hbm
import random

from vm import write


@dataclass
class Task:
    task_id: int                                    # 0
    start_addr: int                                 # 1
    end_addr: int                                   # 2
    part: int                                       # 3
    parts_count: int                                # 4
    part_idx: int                                   # 5
    task_group_id: int                              # 6
    tpc_id: int                                     # 7
    op: int # 0 - write, 1 - read                   | 8
    blob: List[int]                                 # 9       
    canGet: int                                     #10
    state: int #0 - dont run, 1 - run, 2 done       #11
    ticks : int
    
@dataclass
class HbmWorkload:
    workload: int # 0 - write, 1 - read, 2 - nothing    | 0
    ticks: int # when 0 then free                       | 1
    task_id: int                                        # 3

@dataclass
class Tpc:
    id: int
    state: int #0 -free #1 run
    

m_hbm = [0] * 100


for i in range (0, 100):
    start_addr = random.randint(0 , 100)
    memory = random.randint(0, 10)
    end_addr = start_addr + memory
    if end_addr > 100:
        end_addr = 100
    op = random.random(0, 1)
    state = 0
    ticks = random.randint(10, 30)
    parts_count = memory % 10


write([__taskQueue])
for _ in range(50):
    ticks(__workloadTable, )