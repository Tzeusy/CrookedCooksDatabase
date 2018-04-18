import string

import requests
import unittest
import json
import random

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True


class TestServerMethods(unittest.TestCase):
    def setUp(self):
        self.base_address = "http://crookedcooks.herokuapp.com/api/"
        self.tableNumber = "49"


class MenuTestCase(TestServerMethods):
    def test_existent_table(self):
        menu_address = self.base_address + "menu?table_number=" + self.tableNumber
        r = requests.get(menu_address)
        # print("Table 49 test:", r.status_code)
        self.assertEqual(str(r.status_code),"200")

    def test_nonexistent_table(self):
        failedR = requests.get(self.base_address + "menu?table_number=" + "103")
        # print("Nonexistent table test:", failedR.status_code)
        self.assertEqual(str(failedR.status_code),"404")

    def test_valid_json(self):
        menu_address = self.base_address + "menu?table_number=" + self.tableNumber
        r = requests.get(menu_address)
        # print("Table 49 test:", r.status_code)
        # print(r.content.decode("utf-8"))
        self.assertTrue(is_json(r.content.decode("utf-8")))

    # def test_orders(self):
    #     menu_address = self.base_address + "existing_orders" + self.tableNumber
    #     r = requests.get(menu_address)
    #     # print("Table 49 test:", r.status_code)
    #     print(r.content.decode("utf-8"))
    #     self.assertTrue(is_json(r.content.decode("utf-8")))
    # def test_new_menu(self):
    #     new_menu_address = self.base_address + "admin/new_menu?keycode=12345&restaurant_name=Crooked_Cooks"
    #     new_menu_address = "http://localhost:5000/api/" + "admin/new_menu?keycode=12345&restaurant_name=Crooked_Cooks"
    #     menu_address = self.base_address + "menu?table_number=" + self.tableNumber
    #     r = requests.get(menu_address)
    #     print(r.content)
    #     postreq = requests.post(new_menu_address,json ={
    #         "menu":[{"food_category": "Main", "food_id": "123", "name": "2312", "description": "312", "price": "31.2", "currency": "$S*", "image_link": "31", "is_available": True},
    #                 {"food_category": "Main", "food_id": "123", "name": "2312", "description": "312", "price": "3.12", "currency": "$S*", "image_link": "31", "is_available": True},
    #                 {"food_category": "Main", "food_id": "123", "name": "2312", "description": "312", "price": "2.37", "currency": "$S*", "image_link": "31", "is_available": True}]})
    #     # r = requests.post(order_address, json={
    #     #     "orders": [{"food_id": "103", "comment": "testing"},
    #     #                {"food_id": "203", "comment": "onetwothree"},
    #     #                {"food_id": "101", "comment": "SADFSDFSDHFDSSDF"}]})
    #     print(postreq.status_code)
    #     r = requests.get(menu_address)
    #     print(r.content)


class CreateUser(TestServerMethods):
    def test_create_non_crooked_cooks_user(self):
        # Exit in case they already exist
        exit_address = self.base_address + "make_payment?plid=56789&token_id=tok_visa"
        r = requests.get(exit_address)

        print("Testing user for table number 50 <= n < 100")
        register_address = self.base_address + "register?plid=56789&table_number=51"
        print("Visiting " + register_address)
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code),"200")
        self.assertEqual(response, "False")

        # Creating an identical user after first exists should not be possible
        print("Testing repeat visit, if previous session has not closed")
        r = requests.get(register_address)
        print("Visiting " + register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code), "200")
        self.assertEqual(response, "Invalid - entry for customer already exists in table")

        # Make them exit so we can run this test automatically
        # exit_address = self.base_address + "make_payment?plid=56789&token_id=tok_visa"
        r = requests.get(exit_address)
        print("User exiting restaurant")
        print("Visiting " + exit_address)
        response = r.content.decode("UTF-8")

    def test_create_crooked_cooks_user(self):
        # Exit in case they already exist
        exit_address = self.base_address + "make_payment?plid=23456&token_id=tok_visa"
        r = requests.get(exit_address)

        print("Testing user for table number 0 < n < 50")
        register_address = self.base_address + "register?plid=23456&table_number=37&num_people=3"
        r = requests.get(register_address)
        print("Visiting " + register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code), "200")
        self.assertEqual(response, "Entry created with number of people")

        # Creating an identical second user after first exists should not be possible
        print("Testing repeat visit, if previous session has not closed")
        r = requests.get(register_address)
        print("Visiting " + register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code),"200")
        self.assertEqual(response,"Invalid - entry for customer already exists in table")

        # Exit user
        exit_address = self.base_address + "make_payment?plid=23456&token_id=tok_visa"
        print("Test user exiting restaurant")
        print("Visiting "+exit_address)
        r = requests.get(exit_address)
        response = r.content.decode("UTF-8")

    def test_insufficient_data_crooked_cooks(self):
        print("Testing if not enough data was supplied. Should return True")
        register_address = self.base_address + "register?plid=23456&table_number=31"
        print("Visiting " + register_address)
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code), "200")
        self.assertEqual(response, "True")


class UserExperience(TestServerMethods):
    def setUp(self):
        self.base_address = "http://crookedcooks.herokuapp.com/api/"
        print("Creating User 000234")
        register_address = self.base_address + "register?plid=000234&table_number=1&num_people=3"
        print("Visiting " + register_address)
        r = requests.get(register_address)
        self.assertEqual(str(r.status_code), "200")
        order_address = self.base_address + "make_order?plid=000234"
        print("Visiting " + order_address)
        r = requests.post(order_address, json={
            "orders": [{"food_id": "103", "comment": "testing"},
                       {"food_id": "203", "comment": "onetwothree"},
                       {"food_id": "101", "comment": "SADFSDFSDHFDSSDF"}]})
        self.assertEqual(str(r.status_code), "200")

    def tearDown(self):
        payment_address = self.base_address + "make_payment?plid=000234&token_id=tok_visa"
        print("Visiting " + payment_address)
        r = requests.get(payment_address)
        self.assertEqual(str(r.status_code), "200")

    def test_session(self):
        print("Testing status of session page")
        session_address = self.base_address + "get_session"
        print("Visiting " + session_address)
        r = requests.get(session_address)
        self.assertEqual(str(r.status_code), "200")

    def test_valid_json(self):
        print("Testing if session page's JSON is valid")
        session_address = self.base_address + "get_session"
        r = requests.get(session_address)
        print("Visiting " + session_address)
        self.assertTrue(is_json(r.content.decode("utf-8")))

    def test_existing_orders(self):
        print("Testing status of existing orders page")
        orders_page = self.base_address + "existing_orders"
        print("Visiting " + orders_page)
        r = requests.get(orders_page)
        self.assertEqual(str(r.status_code), "200")

    def test_existing_orders_json(self):
        print("Testing existing orders's JSON is valid")
        orders_page = self.base_address + "existing_orders"
        print("Visiting " + orders_page)
        r = requests.get(orders_page)
        self.assertTrue(is_json(r.content.decode("utf-8")))

    def test_existing_individual_order(self):
        orders_page = self.base_address + "existing_orders?plid=000234"
        print("Visiting " + orders_page)
        r = requests.get(orders_page)
        self.assertEqual(str(r.status_code), "200")

    def test_existing_individual_order_json(self):
        orders_page = self.base_address + "existing_orders?plid=000234"
        print("Visiting " + orders_page)
        r = requests.get(orders_page)
        self.assertTrue(is_json(r.content.decode("UTF-8")))

    def test_query_price(self):
        print("Testing price of his orders")
        price_address = self.base_address + "query_price?plid=000234"
        print("Visiting " + price_address)
        r = requests.get(price_address)
        # print(r.content.decode("UTF-8").replace("'",'"'))
        price_information = json.loads(r.content.decode("UTF-8").replace("'", '"'))
        print("Price of his order is " + str(price_information['total_price']) + ", should be 15.4")
        self.assertEqual(price_information['total_price'], 15.4)

    def test_get_time_price(self):
        print("Testing status of get_time_price")
        time_price_link = self.base_address + "get_time_price?plid=000234&table_number=1"
        r = requests.get(time_price_link)
        self.assertEqual(str(r.status_code), "200")

    def test_get_time_price_json(self):
        print("Testing time_price")
        time_price_link = self.base_address + "get_time_price?plid=000234&table_number=1"
        r = requests.get(time_price_link)
        time_and_price = json.loads(r.content.decode("UTF-8").replace("'",'"'))
        self.assertTrue(is_json(json.dumps(time_and_price)))

    def test_set_delivered(self):
        print("Setting set_delivered functionality")
        orders_link = self.base_address + "existing_orders?plid=000234"
        r = requests.get(orders_link)
        previous_order_statuses = r.content.decode("UTF-8")
        print("Before: Orders are " + previous_order_statuses)
        print("Making one instance of order 103 delivered")
        delivered_link = self.base_address + "admin/set_delivered?plid=000234&food_id=103"
        r = requests.get(delivered_link)
        r = requests.get(orders_link)
        later_order_statuses = r.content.decode("UTF-8")
        print("After: Orders are " + later_order_statuses)
        # Crude; but about same speed as doing a dictionary iteration
        self.assertTrue('"food_id":103,"delivered":false' in previous_order_statuses)
        self.assertTrue('"food_id":103,"delivered":true' in later_order_statuses)
        print("Set_delivered test passed")

    def test_set_availability(self):
        print("Testing set_available functionality within the menu")
        make_available_link = self.base_address + "admin/set_availability?boolean=true&food_id=102"
        make_unavailable_link = self.base_address + "admin/set_availability?boolean=false&food_id=102"
        # Initialize as true
        requests.get(make_available_link)

        menu_link = self.base_address + "menu?table_number=49"
        r = requests.get(menu_link)
        menu = r.content.decode("UTF-8").replace("'", '"')
        menu_items = json.loads(menu)['menu']
        for item in menu_items:
            if item['food_id'] == 102:
                # Check if originally true
                self.assertEqual(item['is_available'], True)
        # Set to unavailable
        requests.get(make_unavailable_link)
        r = requests.get(menu_link)
        menu = r.content.decode("UTF-8").replace("'", '"')
        menu_items = json.loads(menu)['menu']
        for item in menu_items:
            if item['food_id'] == 102:
                # Check if false
                self.assertEqual(item['is_available'], False)
        # Set to available
        requests.get(make_available_link)
        r = requests.get(menu_link)
        menu = r.content.decode("UTF-8").replace("'", '"')
        menu_items = json.loads(menu)['menu']
        for item in menu_items:
            if item['food_id'] == 102:
                # Check if true
                self.assertEqual(item['is_available'], True)


class ExtremityTests(TestServerMethods):
    def register_numbers(self):
        customer_id_possibilities = [1,500000,100000000000]
        for customer_id in customer_id_possibilities:
            exit_address = self.base_address + "make_payment?plid={}&token_id=tok_visa".format(customer_id)
            r = requests.get(exit_address)
            register_address = self.base_address + "register?plid={}&table_number=51".format(customer_id)
            print("Visiting " + register_address)
            r = requests.get(register_address)
            response = r.content.decode("UTF-8")
            self.assertEqual(str(r.status_code), "200")
            self.assertEqual(response, "False")
            # Creating an identical user after first exists should not be possible
            print("Testing repeat visit, if previous session has not closed")
            r = requests.get(register_address)
            print("Visiting " + register_address)
            response = r.content.decode("UTF-8")
            self.assertEqual(str(r.status_code), "200")
            self.assertEqual(response, "Invalid - entry for customer already exists in table")
            # Make them exit so we can run this test automatically
            # exit_address = self.base_address + "make_payment?plid=56789&token_id=tok_visa"
            r = requests.get(exit_address)
            print("User exiting restaurant")
            print("Visiting " + exit_address)
            response = r.content.decode("UTF-8")

    def test_user_input(self):
        exit_address = self.base_address + "make_payment?plid={}&token_id=tok_visa".format("000234")
        self.base_address = "http://crookedcooks.herokuapp.com/api/"
        print("Creating User 000234")
        register_address = self.base_address + "register?plid=000234&table_number=1&num_people=3"
        print("Visiting " + register_address)
        r = requests.get(register_address)
        self.assertEqual(str(r.status_code), "200")
        order_address = self.base_address + "make_order?plid=000234"
        print("Visiting " + order_address)
        comments = []
        for i in range(3):
            string_length = random.randrange(0,1000)
            # Random string lengths of up to 1000 chars
            comments.append(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(string_length)))
        r = requests.post(order_address, json={
            "orders": [{"food_id": "103", "comment": comments[0]},
                       {"food_id": "203", "comment": comments[1]},
                       {"food_id": "101", "comment": comments[2]}]})
        self.assertEqual(str(r.status_code), "200")
        orders_page = self.base_address + "existing_orders?plid=000234"
        r = requests.get(orders_page)
        print(r.content.decode("UTF-8"))
        requests.get(exit_address)



if __name__=="__main__":
    # suite = unittest.TestLoader().loadTestsFromTestCase(MenuTestCase)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(CreateUser)
    unittest.TextTestRunner(verbosity=2).run(suite)