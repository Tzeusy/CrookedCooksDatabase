import psycopg2
from initialize_session import flush_database
from connection_pool import ConnectionFromPool

connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')

def get_latest_session(table_number,customer_id):
    with ConnectionFromPool() as cursor:
        # Avoids multiple same-day visits by using only the most recent transaction id. Highest transaction ID
        # will be latest as transaction ID is initialized as SERIAL.
        cursor.execute(
            "SELECT MAX(transaction_id) FROM session WHERE customer_id = {} AND table_number = {}".format(
                customer_id,
                table_number))
        transaction_id = cursor.fetchone()[0]
        return transaction_id

def enter_restaurant(customer_id,table_number,num_people):
    with ConnectionFromPool() as cursor:
        cursor.execute("INSERT INTO session(table_number,customer_id,num_people,start_time) "
                       "VALUES({},{},{},NOW())".format(table_number,customer_id,num_people))

def make_purchase(table_number, customer_id, items):
    transaction_id = get_latest_session(table_number,customer_id)
    with ConnectionFromPool() as cursor:
        for item in items:
            cursor.execute("INSERT INTO purchases(transaction_id,food_id,delivered) "
                           "VALUES({},{},false)".format(transaction_id,item))

def query_price(table_number,customer_id):
    with ConnectionFromPool() as cursor:
        transaction_id = get_latest_session(table_number,customer_id)
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

def end_time(table_number,customer_id):
    with ConnectionFromPool() as cursor:
        latest_transaction_id = get_latest_session(table_number,customer_id)
        cursor.execute("UPDATE session SET end_time = NOW() WHERE session.transaction_id = {}".format(latest_transaction_id))

if __name__ == "__main__":
    flush_database()
    #items are just random food_ids. can find on menuList.
    items = [103,106,303,202]
    items2 = [102,203,306]
    items3 = [100,101,303,301]
    items4 = [201,202,203]
    #enter_restaurant(customer_id,table_number,num_people)
    enter_restaurant(351,8,4)
    enter_restaurant(106,9,2)
    enter_restaurant(918,1,1)
    enter_restaurant(38150,8,9)
    # make_purchase(table_id,customer_id,items)
    make_purchase(8, 351, items)
    make_purchase(9, 106, items2)
    make_purchase(1, 918, items3)
    make_purchase(8, 38150, items4)
    #query_price(table_id,customer_id)
    print("Customer {}: Price is {} by ordering {}".format(351, query_price(8,351)[0], query_price(8,351)[1]))
    print("Customer {}: Price is {} by ordering {}".format(106, query_price(9, 106)[0], query_price(9,106)[1]))
    print("Customer {}: Price is {} by ordering {}".format(918, query_price(1, 918)[0], query_price(1,918)[1]))
    print("Customer {}: Price is {} by ordering {}".format(38150, query_price(8, 38150)[0], query_price(8,38150)[1]))