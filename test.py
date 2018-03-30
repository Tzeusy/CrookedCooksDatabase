from databaseAccessMethods import *
from databaseRequestMethods import *
from random import *
from string import *

# food_options = [100, 101, 102, 103, 104, 105, 106, 201, 202, 203, 301, 302, 303, 304, 305, 306, 307]
# customer_ids = [11111111, 22222222, 33333333, 44444444]
# purchased_items = [[], [], [], []]
# comments = [[], [], [], []]
# rand_str = lambda n: ''.join([choice(ascii_lowercase) for _ in range(n)])
# for i in range(4):
#     num_orders = randint(1, 9)
#     table_number = randint(1, 99)
#     num_people = randint(1, 8)
#     for j in range(num_orders):
#         rand_item = randint(0, len(food_options) - 1)
#         purchased_items[i].append(food_options[rand_item])
#         comments[i].append(rand_str(6))
#
#     enter_restaurant(customer_ids[i], table_number, num_people)
#     make_order(customer_ids[i], purchased_items[i], comments[i])

make_payment(11111111)