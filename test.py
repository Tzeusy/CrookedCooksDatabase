import stripe
from databaseRequestMethods import *
from databaseAccessMethods import *
from random import choice, randint, random
from string import ascii_lowercase

print(get_stats(56789))
print(query_price(56789))