from typing import List
from attr import dataclass
from hbm import Hbm


@dataclass
class Task:
    task_id: int                        # 0
    start_addr: int                     # 1
    end_addr: int                       # 2
    part: int                           # 3
    parts_count: int                    # 4
    part_idx: int                       # 5
    task_group_id: int                  # 6
    tpc_id: int                         # 7
    op: int # 0 - write, 1 - read       | 8
    blob: List[int]                     # 9
    canGet: int                         # 10
    
@dataclass
class HbmWorkload:
    workload: int # 0 - write, 1 - read, 2  | 0
    ticks: int # when 0 then free           | 1
    task_id: int                            # 2
    

m_hbm = [0] * 100