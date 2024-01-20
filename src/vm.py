import random
from typing import List
from typing_extensions import deprecated
from attr import dataclass
import deal


m_hbm = [0] * 100


@dataclass
# not used
class HbmWorkload:
    workload: int   # 0 - write, 1 - read, 2 - nothing  | 0
    ticks: int      # when 0 then free                  | 1
    task_id: int    #                                   | 2


@dataclass
# not used
class Task:
    task_id: int        #                                   | 0
    start_addr: int     #                                   | 1
    end_addr: int       #                                   | 2
    part: int           #                                   | 3
    parts_count: int    #                                   | 4
    part_idx: int       #                                   | 5
    task_group_id: int  #                                   | 6
    tpc_id: int         #                                   | 7
    op: int             # 0 - write, 1 - read               | 8
    blob: List[int]     #                                   | 9       
    canGet: int         #                                   | 10
    state: int          # 0 - dont run, 1 - run, 2 - done   | 11

# таблица занятости ячеек памяти
workloadsTable = []
for i, cell in enumerate(m_hbm):
    workloadsTable.append([2, 0, 0])
    
# таблица очереди тасок
tasksQueue: List[int] = []

# костыль для имитации асинхронности чтений
# task_id   | 0
# result    | 1
read_tasks_results = []


# Создание id для новой задачи
@deal.pre(lambda taskQueue: len(taskQueue) >= 0)
@deal.post(lambda result: result >= 0)
def nextId(taskQueue: List[List[int]]) -> int:
    if len(taskQueue) == 0:
        return 0
    else:
        return taskQueue[len(taskQueue) - 1][0] + 1


# 1 тик системы
def tick(workloadTable: List[List[int]], taskQueues: List[List[int]], read_tasks_result: List[List[int]]) -> None:
    filtered_tasks = []
    for task in taskQueues:
        # TODO проверить индексы, возможно написать комментарий
        if(task[8] == 1 and task[5] == 1):
            filtered_tasks.append(task)
    
    for task in filtered_tasks:
        # если таска еще не в работе
        print(task)
        if task[11] == 0:
            isFree = True
            for i in range(task[1], task[2] + 1):
                # TODO если память читается а мы хотим записать добавить проверку
                
                # если нужная ячейка сейчас на записи, то таску нельзя брать в работу
                if workloadTable[i][0] == 0:
                    isFree = False
                    break
                
            # если таску можно взять в работу            
            if isFree:
                # иммитация случайности лдолготы выполнения
                ticktack = random.randint(10,30)
                # запись информации о занятости ячеек
                for i in range(task[1], task[2] + 1):
                    workloadTable[i][0] = task[8]
                    workloadTable[i][1] = ticktack
                    workloadTable[i][2] = task[0]  
                task[11] = 1              
        
        # если таска в работе        
        elif task[11] == 1:
            # TODO ???
            if task[10] == 0:
                read_result = []
                # уменьшаем для всех ячеек 'время занятости'
                for i in range(task[1], task[2] + 1):
                    workloadTable[i][0] -= 1          
                    if workloadTable[i][1] == 0:
                        # в нулевой тик завершить операцию
                        workloadTable[i][0] == 2
                        task[11] = 2
                         # если была операция записи
                        if task[8] == 0:
                            # запись информации из blob-а таски в hbm
                            m_hbm[i] = task[9][i - task[1]]                            
                        # если была операция записи
                        else:
                            # заполнение результата чтения
                            read_result.append(task[9][i - task[1]]) 
                # tесли было чтение и оно завершено, запись результата   
                if len(read_result) != 0:
                    read_tasks_result.append([task[0], read_result])                                                       
                
        # избавляемся от выполненных задач
        condition = lambda x: x[11] == 2
        # TODO what is it
        #taskQueue = [x for x in taskQueue if not condition(x)]



@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id: start_addr >= 0)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id: start_addr < 100)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id: end_addr >= 0)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id: end_addr < 100)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id: start_addr < end_addr)
def read(
    taskQueue: list[list[int]],
    start_addr: int,
    end_addr: int,
    part: int,
    parts_count: int,
    task_group_id: int,
    tcp_id: int
) -> int:
    task_id = nextId(taskQueue)
    taskQueue.append([task_id, start_addr, end_addr, part, parts_count, part, task_group_id, tcp_id, 1, [], 0, 0])
    # если пришел последний пакет из группы
    if part == parts_count:
        # то для всех таск
        for i in range(len(taskQueue)):
            # из этой группы
            if taskQueue[i][6] == task_group_id:
                # разрешаем таски на взятие в работу
                taskQueue[i][10] = 1
    return task_id


@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id, blob: start_addr >= 0)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id, blob: start_addr < 100)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id, blob: end_addr >= 0)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id, blob: end_addr < 100)
@deal.pre(lambda taskQueue, start_addr, end_addr, part, parts_count, task_group_id, tcp_id, blob: start_addr < end_addr)
def write(
    taskQueue: List[List[int]],
    start_addr: int,
    end_addr: int,
    part: int,
    parts_count: int,
    task_group_id: int,
    tcp_id: int,
    blob: List[int]
) -> None:
    taskQueue.append([nextId(taskQueue), start_addr, end_addr, part, parts_count, part, task_group_id, tcp_id, 0, blob, 0, 0])
    # если пришел последний пакет из группы
    if part == parts_count:
        # то для всех таск
        for i in range(len(taskQueue)):
            # из этой группы
            if taskQueue[i][6] == task_group_id:
                # разрешаем таски на взятие в работу
                taskQueue[i][10] = 1


# TODO del
# проверка что методы из этого файла подцеаляются во время deal prove
@deal.pre(lambda n: n >= 0)
@deal.post(lambda n: n > 0)
def deal_test(n: int) -> None:
    return -1