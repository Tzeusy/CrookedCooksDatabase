import psycopg2
from initialize_session import flush_database
from connection_pool import ConnectionFromPool
from datetime import datetime

connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')

def enter_restaurant(customer_id,table_number,num_people):
    #Creates an entry in the SESSION table. Num people is necessary for Crooked Cooks specifically.
    with ConnectionFromPool() as cursor:
        transaction_id = int(datetime.now().microsecond*customer_id/1000)
        print("Creating a new session, with transaction id",transaction_id)
        cursor.execute("INSERT INTO session(transaction_id,table_number,customer_id,num_people,start_time) "
                       "VALUES({},{},{},{},NOW())".format(transaction_id, table_number,customer_id,num_people))

def make_order(customer_id,items,comments):
    #Creates an entry in the PURCHASES table. Each entry requires a customer id (int), items (int array), and comments (text array)
    transaction_id, _, _, _, _ = get_stats(customer_id)
    with ConnectionFromPool() as cursor:
        for i in range (len(items)):
            cursor.execute("INSERT INTO purchases(transaction_id,food_id,delivered,comments) "
                           "VALUES({},{},false,'{}')".format(transaction_id,items[i],comments[i]))

def order_satisfied(customer_id,food_id,comment):
    with ConnectionFromPool() as cursor:
        cursor.execute("UPDATE purchases SET delivered = true "
                       "WHERE food_id = {} AND comments = '{}' AND customer_id = {}"
                       .format(food_id,comment,customer_id))

def query_price(customer_id):
    with ConnectionFromPool() as cursor:
        transaction_id, _, _, _, _ = get_stats(customer_id)
        #Can actually have this be a constantly existing VIEW in the database. I'll leave it as is for
        # the moment though - not sure how costly sql accesses are
        cursor.execute("DROP VIEW IF EXISTS total_transaction_cost")
        cursor.execute("CREATE VIEW total_transaction_cost AS "
                       "SELECT session.transaction_id,SUM(price) FROM session "
                       "INNER JOIN purchases ON purchases.transaction_id = session.transaction_id "
                       "INNER JOIN menu ON purchases.food_id = menu.food_id "
                       "GROUP BY session.transaction_id")
        cursor.execute("SELECT sum FROM total_transaction_cost WHERE transaction_id={}".format(transaction_id))
        itemSum = cursor.fetchone()[0]
        cursor.execute("SELECT (DATE_PART('day', NOW() - session.start_time) * 24 + "
                                   "DATE_PART('hour', NOW() - session.start_time)) * 60 + "
                                   "DATE_PART('minute', NOW() - session.start_time) as time_difference_minutes FROM session "
                                   "WHERE transaction_id={}".format(transaction_id))
        #For crooked cooks, it's $2 per hour
        timePrice = int(cursor.fetchone()[0]/60+1)*2
        totalPrice = itemSum+timePrice

        cursor.execute("SELECT session.transaction_id, menu.name FROM session "
                       "INNER JOIN purchases ON purchases.transaction_id = session.transaction_id "
                       "INNER JOIN menu ON menu.food_id = purchases.food_id "
                       "WHERE session.transaction_id = {} "
                       "ORDER BY transaction_id".format(transaction_id))

        orderHistory = cursor.fetchall()
        items = [orders[1] for orders in orderHistory]
        return (totalPrice,items)

def exit_restaurant(customer_id):
    with ConnectionFromPool() as cursor:
        transaction_id, table_number, _, num_people, start_time = get_stats(customer_id)
        totalPrice, orders = query_price(customer_id)
        orderString = "'"
        orderString += '{"'+'","'.join(item for item in orders)+'"}'
        orderString+="'"
        cursor.execute("INSERT INTO history(transaction_id, food_orders, start_time, end_time, total_price)"
                       "VALUES ({},{},to_timestamp('{}','YYYY-MM-DD HH:MI:SS'),NOW(),{})".format(transaction_id,orderString,start_time,totalPrice))
        cursor.execute("DELETE FROM session WHERE transaction_id = {}".format(transaction_id))
        cursor.execute("DELETE FROM purchases WHERE transaction_id = {}".format(transaction_id))

def get_stats(customer_id):
    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT * FROM session WHERE customer_id = {}".format(customer_id))
        item = cursor.fetchall()[0]
        transaction_id = item[1]
        table_number = item[2]
        customer_id = item[3]
        num_people = item[4]
        start_time = item[5]
        return transaction_id,table_number,customer_id,num_people,start_time

if __name__ == "__main__":
    # flush_database()
    #items are just random food_ids. can find on menuList.
    items = [103,106,303,202]
    items2 = [102,203,306]
    items3 = [100,101,303,301]
    items4 = [201,202,203]
    #enter_restaurant(customer_id,table_number,num_people)
    comments1 = ["hi","wat",None,"wat"]
    comments2 = ["hi", "wat", None, "wat"]
    comments3 = ["hi", "wat", None, "wat"]
    comments4 = ["hi", "wat", None, "wat"]
    enter_restaurant(351,8,4)
    enter_restaurant(106,9,2)
    enter_restaurant(918,1,1)
    enter_restaurant(38150,8,9)
    # make_order(table_id,customer_id,items)
    make_order(351, items, comments1)
    make_order(106, items2,comments2)
    make_order(918, items3,comments3)
    make_order(38150, items4,comments4)
    #query_price(table_id,customer_id)
    print("Customer {}: Price is {} by ordering {}".format(351, query_price(351)[0], query_price(351)[1]))
    print("Customer {}: Price is {} by ordering {}".format(106, query_price(106)[0], query_price(106)[1]))
    print("Customer {}: Price is {} by ordering {}".format(918, query_price(918)[0], query_price(918)[1]))
    print("Customer {}: Price is {} by ordering {}".format(38150, query_price(38150)[0], query_price(38150)[1]))
    # print(get_stats(38150))
    # exit_restaurant(351)
    # exit_restaurant(106)
    # exit_restaurant(918)
    # exit_restaurant(38150)