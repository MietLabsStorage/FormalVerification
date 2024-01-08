from test_main import two_writes_with_one_part

# @dataclass
# class Tpc:
#     id: int
#     state: int #0 -free #1 run

# for i in range (0, 100):
#     start_addr = random.randint(0 , 100)
#     memory = random.randint(0, 10)
#     end_addr = start_addr + memory
#     if end_addr > 100:
#         end_addr = 100
#     op = random.random(0, 1)
#     state = 0
#     ticks = random.randint(10, 30)
#     parts_count = memory % 10


# write([__taskQueue])
# for _ in range(50):
#     ticks(__workloadTable, )

r1 = two_writes_with_one_part(
    0, 5, [1, 2, 3, 4, 5, 6],
    3, 6, [0, 7, 2, 9]
)

print(r1)