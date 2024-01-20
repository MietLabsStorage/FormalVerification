from typing import List
import deal
from vm import write as vm_write
from vm import read as vm_read
from vm import tasksQueue as vm_taskQueue
from vm import read_tasks_results as vm_read_tasks_results
from vm import workloadsTable as vm_workloadsTable
from vm import tick


def enshure_addrs_intersect(start_addr1, end_addr1, start_addr2, end_addr2):
    if start_addr1 < start_addr2:
        return start_addr2 <= end_addr1
    else:
        return start_addr1 <= end_addr2


pre_contracts_addrs = deal.chain(
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: 0 <= start_addr1 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: 0 <= end_addr1 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: start_addr1 < end_addr1),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: 0 <= start_addr2 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: 0 <= end_addr2 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: start_addr2 < end_addr2),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: enshure_addrs_intersect(start_addr1, end_addr1, start_addr2, end_addr2)),
)

pre_contracts_addrs_parts = deal.chain(
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= start_addr1 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= end_addr1 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: start_addr1 < end_addr1),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= start_addr2 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= end_addr2 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: start_addr2 < end_addr2),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= start_addr3 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= end_addr3 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: start_addr3 < end_addr3),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= start_addr4 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: 0 <= end_addr4 <= 100),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: start_addr4 < end_addr2),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: not enshure_addrs_intersect(start_addr1, end_addr1, start_addr2, end_addr2)),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: enshure_addrs_intersect(start_addr1, end_addr1, start_addr3, end_addr3)),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: not enshure_addrs_intersect(start_addr3, end_addr3, start_addr4, end_addr4)),
	deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: enshure_addrs_intersect(start_addr4, end_addr4, start_addr2, end_addr2)),
)

pre_contracts_parts = deal.chain(
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob1) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob1) <= 10),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob2) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob2) <= 10),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob1) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob1) <= 10),    
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob2) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, start_addr3, end_addr3, blob3, start_addr4, end_addr4, blob4: len(blob2) <= 10),
)

pre_contracts_noparts = deal.chain(
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob1) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob1) <= 10),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob2) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob2) <= 10),
)


@pre_contracts_addrs
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def two_writes_with_one_part(start_addr1: int, end_addr1: int, blob1: List[int], start_addr2: int, end_addr2: int, blob2: List[int]) -> List[int]:
    # пишем 1 и пишем 2
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr2, end_addr2, 1, 1, 2, 2, blob2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40 * 2):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 1
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 2
    idx2 = vm_read(vm_taskQueue, start_addr2, end_addr2, 1, 1, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    
    return result1 == blob1 or result2 == blob2


@pre_contracts_addrs
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def read_and_write_with_one_part(start_addr1: int, end_addr1: int, blob1: List[int], start_addr2: int, end_addr2: int, blob2: List[int]) -> List[int]:
    # записываем 1
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # читаем 1 и пишем 2 
    vm_write(vm_taskQueue, start_addr2, end_addr2, 1, 1, 2, 2, blob2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40 * 2):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # читаем 2
    idx2 = vm_read(vm_taskQueue, start_addr2, end_addr2, 1, 1, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    
    return result1 == blob1 or result2 == blob2


@pre_contracts_addrs
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def two_reads_with_one_part(start_addr1: int, end_addr1: int, blob1: List[int], start_addr2: int, end_addr2: int, blob2: List[int]) -> List[int]:
    # записываем 1
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # читаем 1 и читаем 2 
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    idx2 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 1, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40 * 2):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    
    return result1 == blob1 and result2 == blob1


@pre_contracts_addrs_parts
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def two_writes_with_two_part(
    start_addr1: int, end_addr1: int, blob1: List[int], 
    start_addr2: int, end_addr2: int, blob2: List[int],
    start_addr3: int, end_addr3: int, blob3: List[int],
    start_addr4: int, end_addr4: int, blob4: List[int],
    ) -> List[int]:
    # пишем 1, пишем 2, пишем 3, пишем 4
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 2, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr2, end_addr2, 2, 2, 1, 1, blob2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    vm_write(vm_taskQueue, start_addr3, end_addr3, 1, 2, 2, 2, blob3)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr4, end_addr4, 2, 2, 2, 2, blob4)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40 * 3):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 1
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 2, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 2
    idx2 = vm_read(vm_taskQueue, start_addr2, end_addr2, 2, 2, 1, 1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 3
    idx3 = vm_read(vm_taskQueue, start_addr3, end_addr3, 1, 2, 2, 2)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 4
    idx4 = vm_read(vm_taskQueue, start_addr4, end_addr4, 2, 2, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    result3 = [x for x in vm_read_tasks_results if x[0] == idx3][0][1]
    result4 = [x for x in vm_read_tasks_results if x[0] == idx4][0][1]
    
    return result1 == blob1 and result2 == blob2 or result3 == blob3 and result4 == blob4


@pre_contracts_addrs_parts
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def read_and_write_with_two_part(
    start_addr1: int, end_addr1: int, blob1: List[int], 
    start_addr2: int, end_addr2: int, blob2: List[int],
    start_addr3: int, end_addr3: int, blob3: List[int],
    start_addr4: int, end_addr4: int, blob4: List[int],
    ) -> List[int]:
    # пишем 1, пишем 2
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 2, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr2, end_addr2, 2, 2, 1, 1, blob2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 1, читаем 2, пишем 3, пишем 4
    vm_write(vm_taskQueue, start_addr3, end_addr3, 1, 2, 2, 2, blob4)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr4, end_addr4, 2, 2, 2, 2, blob4)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)          
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 2, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    idx2 = vm_read(vm_taskQueue, start_addr2, end_addr2, 2, 2, 1, 1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)     
    for _ in range(40 * 4):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 3
    idx3 = vm_read(vm_taskQueue, start_addr3, end_addr3, 1, 2, 2, 2)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 4
    idx4 = vm_read(vm_taskQueue, start_addr4, end_addr4, 2, 2, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    result3 = [x for x in vm_read_tasks_results if x[0] == idx3][0][1]
    result4 = [x for x in vm_read_tasks_results if x[0] == idx4][0][1]
    
    return result1 == blob1 and result2 == blob2 or result3 == blob3 and result4 == blob4


@pre_contracts_addrs_parts
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def two_writes_with_two_part(
    start_addr1: int, end_addr1: int, blob1: List[int], 
    start_addr2: int, end_addr2: int, blob2: List[int],
    start_addr3: int, end_addr3: int, blob3: List[int],
    start_addr4: int, end_addr4: int, blob4: List[int],
    ) -> List[int]:
    # пишем 1, пишем 2
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 2, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr2, end_addr2, 2, 2, 1, 1, blob2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)      
    for _ in range(40 * 2):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    # читаем 1, читаем 2, читаем 3, читаем 4
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 2, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    idx2 = vm_read(vm_taskQueue, start_addr2, end_addr2, 2, 2, 1, 1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    idx3 = vm_read(vm_taskQueue, start_addr3, end_addr3, 1, 2, 2, 2)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    idx4 = vm_read(vm_taskQueue, start_addr4, end_addr4, 2, 2, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)    
    for _ in range(40 * 4):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    result3 = [x for x in vm_read_tasks_results if x[0] == idx3][0][1]
    result4 = [x for x in vm_read_tasks_results if x[0] == idx4][0][1]
    
    return result1 == blob1 and result2 == blob2 or result3 == blob3 and result4 == blob4


# TODO del
# проверка что методы из этого файла подцеаляются во время deal prove
@deal.pre(lambda n: n >= 0)
@deal.post(lambda n: n > 0)
def deal_test(n: int) -> None:
    return -1