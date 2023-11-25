from vm import Vm


class Tpc:
    def __init__(self, id: int, vm: Vm):
        self.id = id

    def read(start_addr, end_addr, part, parts_count):
        print(start_addr, end_addr)
    
    def write(start_addr, end_addr):
        print(start_addr, end_addr)