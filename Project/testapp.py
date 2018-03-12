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
        self.baseaddress = "http://10.12.184.102:4995/"
        self.tableNumber = "49"

class menuTestCase(TestServerMethods):
    def test_existentTable(self):
        menuaddress = self.baseaddress + "api/menu?tablenumber=" + self.tableNumber
        r = requests.get(menuaddress)
        # print("Table 49 test:", r.status_code)
        self.assertEqual(str(r.status_code),"200")

    def test_valid_json(self):
        menuaddress = self.baseaddress + "api/menu?tablenumber=" + self.tableNumber
        r = requests.get(menuaddress)
        # print("Table 49 test:", r.status_code)
        print(r.content.decode("utf-8"))
        self.assertTrue(is_json(r.content.decode("utf-8")))

    def test_nonexistentTable(self):
        failedR = requests.get(self.baseaddress + "api/menu?tablenumber=" + "52")
        # print("Nonexistent table test:", failedR.status_code)
        self.assertEqual(str(failedR.status_code),"404")

if __name__=="__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServerMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)