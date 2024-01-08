from typing import List
import deal
from vm import write as vm_write
from vm import read as vm_read
from vm import taskQueue as vm_taskQueue
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

# pre_contracts_parts = deal.chain(
#     deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: parts_count1 > 0 and parts_count1 < 10),
#     deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: parts_count2 > 0 and parts_count2 < 10),
    
#     deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob1) > 0),
#     deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, parts_count1: len(blob1) <= 10 * parts_count1 and len(blob1) > 10 * (parts_count1 - 1)),
#     deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob2) > 0),
#     deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2, parts_count2: len(blob2) <= 10 * parts_count2 and len(blob2) > 10 * (parts_count2 - 1)),
# )

pre_contracts_noparts = deal.chain(
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob1) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob1) <= 10),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob2) > 0),
    deal.pre(lambda start_addr1, end_addr1, blob1, start_addr2, end_addr2, blob2: len(blob2) <= 10),
)

# TODO зосдать тестовые методы:
# Две записи на смежную память (для однопакетных)
# Записать память. После этого одновременно читать и изменять её (для однопакетных)
# 
# Две записи на смежную память (для многопакетных)
# Записать память. После этого одновременно читать и изменять её (для многопакетных)
#
# Записать память. После этого одновременно читать для двух устройств её (для однопакетных)
# Записать память. После этого одновременно читать для двух устройств её (для многопакетных)

@pre_contracts_addrs
@pre_contracts_noparts
@deal.post(lambda result: result == True)
def two_writes_with_one_part(start_addr1: int, end_addr1: int, blob1: List[int], start_addr2: int, end_addr2: int, blob2: List[int]) -> List[int]:
    vm_write(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1, blob1)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    vm_write(vm_taskQueue, start_addr2, end_addr2, 1, 1, 2, 2, blob2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
        
    idx1 = vm_read(vm_taskQueue, start_addr1, end_addr1, 1, 1, 1, 1)    
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    idx2 = vm_read(vm_taskQueue, start_addr2, end_addr2, 1, 1, 2, 2)
    tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    for _ in range(40):
        tick(vm_workloadsTable, vm_taskQueue, vm_read_tasks_results)
    
    # получаем результаты чтений по аддресам на которые записывали    
    result1 = [x for x in vm_read_tasks_results if x[0] == idx1][0][1]
    result2 = [x for x in vm_read_tasks_results if x[0] == idx2][0][1]
    
    return result1 == blob1 or result2 == blob2
