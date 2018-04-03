from connection_pool import ConnectionFromPool
import json

from databaseAccessMethods import *


def getMenu(table_number):
    restaurant_name = "Crooked Cooks"
    restaurant_image = "https://i.imgur.com/XvlwlIn.jpg"

    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'menu'")
        menu_headers = cursor.fetchall()
        cursor.execute("SELECT * FROM menu")
        non_parsed_array = cursor.fetchall()

    final_string = jsonify_reply(menu_headers, non_parsed_array)
    full_json = '{{"name":"{}","imagehyperlink":"{}","menu":[{}]}}'.format(restaurant_name, restaurant_image, final_string)
    return full_json


def getOrders(customer_id=None):
    sql_command = "SELECT session.table_number,session.start_time," \
                  "menu.price, purchases.food_id,purchases.delivered, purchases.comments, purchases.additional_price " \
                  "FROM session INNER JOIN purchases ON purchases.transaction_id = session.transaction_id" \
                  " INNER JOIN menu ON purchases.food_id = menu.food_id "
    if customer_id is not None:
        sql_command += "WHERE session.customer_id = {}".format(customer_id)

    with ConnectionFromPool() as cursor:
        # cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'session'");
        menu_headers = [("table_number", "integer"), ("start_time", "timestamp without time zone"),
                        ("price", "numeric(4, 2)"), ("food_id", "integer"), ("delivered", "boolean"),
                        ("comments", "text"), ("additional_price", "numeric(4,2)")]
        cursor.execute(sql_command)
        non_parsed_array = cursor.fetchall()
    final_string = '{{"orders":[{}]}}'.format(jsonify_reply(menu_headers, non_parsed_array))
    return final_string


def get_time_and_price(customer_id, table_number):
    print("Getting time and price")
    transaction_id, _, _, _, _ = get_stats(customer_id)
    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT DATE_PART('hour',NOW() - start_time) FROM session WHERE transaction_id = {}".format(
            transaction_id))
        hours = int(cursor.fetchone()[0])
        cursor.execute("SELECT DATE_PART('minute',NOW() - start_time) FROM session WHERE transaction_id = {}"
                       .format(transaction_id))
        minutes = int(cursor.fetchone()[0])
        if 0 < table_number < 50:
            return "{"+'"time_price":{},"hours":{},"minutes":{}'.format(2 * (hours + 1), hours, minutes)+"}"
        elif 50 <= table_number < 100:
            return "{"+'"time_price":{},"hours":{},"minutes":{}'.format(0 * (hours + 1), hours, minutes)+"}"
        else:
            return False


def get_session():
    sql_command = "SELECT * FROM session"
    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'session'")
        session_headers = cursor.fetchall()
        cursor.execute(sql_command)
        session_array = cursor.fetchall()
    final_string = '{{"session":[{}]}}'.format(jsonify_reply(session_headers, session_array))
    return final_string


def jsonify_reply(headers, row_information):
    # Returns a string in {"abc":"def","efg":"hij",..},{"abc":"def","efg":"hij",..},... format

    # Presumes headers is in [(column_name,data_type),...] format
    # Presumes row information is in [(elem1, elem2,..n),...] format where n=number of columns

    info_array = []
    for i in range(len(row_information)):
        element_info = "{"
        for j in range(len(headers)):
            # LEFT ELEMENT: Header will definitely be in string format
            element_info += '"'
            element_info += headers[j][0]
            element_info += '"'

            element_info += ":"
            # RIGHT ELEMENT: Data may not necessarily be in string format.
            # May need to add apostrophes to the column information, if it is a STRING or a ENUM
            if headers[j][1] == 'text' or headers[j][1] == 'USER-DEFINED' or 'timestamp' in headers[j][1]:
                element_info += '"'
            # True needs to be converted to true, same for False to false >.>
            if headers[j][1] == 'boolean':
                element_info += str(row_information[i][j]).lower()
            else:
                element_info += str(row_information[i][j])
            if headers[j][1] == 'text' or headers[j][1] == 'USER-DEFINED' or 'timestamp' in headers[j][1]:
                element_info += '"'
            if j != len(headers)-1:
                element_info += ","
        element_info += "}"
        info_array.append(element_info)
    final_reply = ",".join(element for element in info_array)
    return final_reply


if __name__ == "__main__":
    print(getMenu(49))
    # myNiceText = json.loads(get_session(49))
    # print(json.dumps(myNiceText, sort_keys=True,indent = 4, separators = (',', ': ')))
