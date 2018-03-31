import stripe
from databaseRequestMethods import *
from databaseAccessMethods import *
from random import choice, randint, random
from string import ascii_lowercase
import requests

# print(query_price(234))
base_address = "https://crookedcooks.herokuapp.com/api/"
print("Testing query price")
print("Creating User 000234")
register_address = base_address + "register?plid=000234&table_number=1&num_people=3"
r = requests.get(register_address)
print("Visiting " + register_address)
print("User created; now making orders")
order_address = base_address + "make_order?plid=000234"
print("Visiting " + order_address)
r = requests.post(order_address, json={
    "orders": [{"food_id": "103", "comment": "testing"},
               {"food_id": "203", "comment": "onetwothree"},
               {"food_id": "101", "comment": "SADFSDFSDHFDSSDF"}]})
print("Orders made; retrieving orders")
existing_orders_address = base_address + "existing_orders?plid=000234"
print("Visiting " + existing_orders_address)
r = requests.get(existing_orders_address)
print(r.content)
print("Testing price of his orders")
price_address = base_address + "query_price?plid=000234"
print("Visiting " + price_address)
r = requests.get(price_address)
print(r.content.decode("UTF-8").replace("'",'"'))
# price_information = json.loads(r.content.decode("UTF-8"))
# print("Price of his order is " + price_information['total_price'])
# make_payment("000234")

