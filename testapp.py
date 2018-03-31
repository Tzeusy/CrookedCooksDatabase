import requests
import unittest
import json

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


class CreateUser(TestServerMethods):
    def test_create_non_crooked_cooks_user(self):
        register_address = self.base_address + "register?plid=56789&table_number=51"
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code),"200")
        self.assertEqual(response, "Entry created with number of people")

        #Creating an identical second user after first exists should not be possible
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code), "200")
        self.assertEqual(response, "Invalid - entry for customer already exists in table")

        #Make them exit so we can run this test automatically
        exit_address = self.base_address + "make_payment?plid=56789&token_id=tok_visa"
        r = requests.get(exit_address)

    def test_create_crooked_cooks_user(self):
        register_address = self.base_address + "register?plid=23456&table_number=37&num_people=3"
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code), "200")
        self.assertEqual(response, "Entry created with number of people")

        # Creating an identical second user after first exists should not be possible
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code),"200")
        self.assertEqual(response,"Invalid - entry for customer already exists in table")

        #Exit user
        exit_address = self.base_address + "make_payment?plid=23456&token_id=tok_visa"
        r = requests.get(exit_address)

    def test_insufficient_data_crooked_cooks(self):
        register_address = self.base_address + "register?plid=23456&table_number=31"
        r = requests.get(register_address)
        response = r.content.decode("UTF-8")
        self.assertEqual(str(r.status_code), "200")
        self.assertEqual(response, "True")


class TestStatusCodes(TestServerMethods):
    def test_session(self):
        session_address = self.base_address + "get_session"
        r = requests.get(session_address)
        self.assertEqual(str(r.status_code), "200")

    def test_valid_json(self):
        session_address = self.base_address + "get_session"
        r = requests.get(session_address)
        # print("Table 49 test:", r.status_code)
        self.assertTrue(is_json(r.content.decode("utf-8")))

    def test_existing_orders(self):
        session_address = self.base_address + "get_session"
        r = requests.get(session_address)
        self.assertEqual(str(r.status_code), "200")

if __name__=="__main__":
    # suite = unittest.TestLoader().loadTestsFromTestCase(MenuTestCase)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(CreateUser)
    unittest.TextTestRunner(verbosity=2).run(suite)