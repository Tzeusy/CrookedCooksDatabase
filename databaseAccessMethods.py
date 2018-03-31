import psycopg2
from initialize_session import flush_database
from connection_pool import ConnectionFromPool
from datetime import datetime
import stripe


def enter_restaurant(customer_id,table_number,num_people):
    # Creates an entry in the SESSION table. Num people is necessary for Crooked Cooks specifically.
    # If already in restaurant, return ERROR.
    print("Testing Enter Restaurant")
    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT * FROM session "
                       "WHERE customer_id = {}".format(customer_id))
        results = cursor.fetchall()
        # Checking if already in database; if already in database, return negative
        if len(results) > 0:
            return -1

    with ConnectionFromPool() as cursor:
        if(customer_id>1000000000):
            transaction_id = int(datetime.now().microsecond*customer_id/100000000)
        else:
            transaction_id = int(datetime.now().microsecond * customer_id / 1000000)
        print("Creating a new session, with transaction id",transaction_id)
        print(transaction_id)
        print(table_number)
        print(customer_id)
        print(num_people)
        cursor.execute("INSERT INTO session(transaction_id,table_number,customer_id,num_people,start_time) "
                       "VALUES({},{},{},{},NOW())".format(transaction_id, table_number,customer_id,num_people))
        print("Creation success")
    return 1


def make_order(customer_id,items,comments):
    #Creates an entry in the PURCHASES table. Each entry requires a customer id (int), items (int array), and comments (text array)
    transaction_id, _, _, _, _ = get_stats(customer_id)
    with ConnectionFromPool() as cursor:
        for i in range (len(items)):
            cursor.execute("INSERT INTO purchases(transaction_id,food_id,delivered,comments,additional_price) "
                           "VALUES({},{},false,'{}',0)".format(transaction_id,items[i],comments[i]))


def order_satisfied(customer_id,food_id,comment):
    transaction_id, _, _, _, _ = get_stats(customer_id)
    sql_command = "WITH cte AS ( " \
                 "SELECT default_id " \
                 "FROM purchases " \
                 "WHERE transaction_id = {} AND food_id = {} AND comments = '{}' " \
                 "LIMIT 1) " \
                 "UPDATE purchases s " \
                 "SET delivered=true " \
                 "FROM cte " \
                 "WHERE s.default_id = cte.default_id".format(transaction_id,food_id,comment)
    with ConnectionFromPool() as cursor:
        for i in range (len(items)):
            cursor.execute(sql_command)
    print("One Order satisfied")


def edit_purchase(customer_id,food_id,comment,additional_price):
    transaction_id, _, _, _, _ = get_stats(customer_id)
    sql_command = "WITH cte AS ( " \
                  "SELECT default_id " \
                  "FROM purchases " \
                  "WHERE transaction_id = {} AND food_id = {} AND comments = '{}' " \
                  "LIMIT 1) " \
                  "UPDATE purchases s " \
                  "SET additional_price = {} " \
                  "FROM cte " \
                  "WHERE s.default_id = cte.default_id".format(transaction_id,food_id,comment,additional_price)
    print('adding additional price for custom order')
    with ConnectionFromPool() as cursor:
        cursor.execute(sql_command)
    print("Order Price changed")


def set_delivered(customer_id,food_id):
    transaction_id, _, _, _, _ = get_stats(customer_id)
    sql_command = "UPDATE purchases SET delivered = true WHERE " \
                  "CTID IN (SELECT CTID FROM purchases WHERE transaction_id = {} " \
                  "AND delivered = false AND food_id = {} LIMIT 1)".format(transaction_id,food_id)
    with ConnectionFromPool() as cursor:
        cursor.execute(sql_command)
        return True


def query_price(customer_id):
    #Returns totalPrice, timeSpent, orders, customPrice
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
        cursor.execute("DROP VIEW IF EXISTS total_comment_cost")
        cursor.execute("CREATE VIEW total_comment_cost AS "
                       "SELECT session.transaction_id,SUM(additional_price) FROM session "
                       "INNER JOIN purchases ON purchases.transaction_id = session.transaction_id "
                       "INNER JOIN menu ON purchases.food_id = menu.food_id "
                       "GROUP BY session.transaction_id")
        cursor.execute("SELECT sum FROM total_transaction_cost WHERE transaction_id={}".format(transaction_id))
        # print(cursor.fetchall())
        cursor_info = cursor.fetchone()
        if cursor_info is not None:
            item_sum = cursor_info[0]
            cursor.execute("SELECT sum FROM total_comment_cost WHERE transaction_id={}".format(transaction_id))
            comments_sum = cursor.fetchone()[0]
            if comments_sum is None:
                comments_sum=0
        else:
            item_sum = 0
            comments_sum = 0
        cursor.execute("SELECT (DATE_PART('day', NOW() - session.start_time) * 24 + "
                                   "DATE_PART('hour', NOW() - session.start_time)) * 60 + "
                                   "DATE_PART('minute', NOW() - session.start_time) as time_difference_minutes FROM session "
                                   "WHERE transaction_id={}".format(transaction_id))
        #For crooked cooks, it's $2 per hour
        timeSpent = int(cursor.fetchone()[0]/60+1)
        timePrice = timeSpent*2
        totalPrice = item_sum+timePrice+comments_sum

        cursor.execute("SELECT session.transaction_id, menu.name FROM session "
                       "INNER JOIN purchases ON purchases.transaction_id = session.transaction_id "
                       "INNER JOIN menu ON menu.food_id = purchases.food_id "
                       "WHERE session.transaction_id = {} "
                       "ORDER BY transaction_id".format(transaction_id))

        orderHistory = cursor.fetchall()
        items = [orders[1] for orders in orderHistory]
        # Returns totalPrice, timeSpent, orders, customPrice
        return (totalPrice,timeSpent,items,comments_sum)


def exit_restaurant(customer_id):
    print("Customer {} exiting Restaurant".format(customer_id))
    with ConnectionFromPool() as cursor:
        transaction_id, table_number, _, num_people, start_time = get_stats(customer_id)
        totalPrice, _, orders,_ = query_price(customer_id)
        orderString = "'"
        orderString += '{"'+'","'.join(item for item in orders)+'"}'
        orderString+="'"
        cursor.execute("INSERT INTO history(transaction_id, customer_id, food_orders, start_time, end_time, total_price)"
                       "VALUES ({},{},{},to_timestamp('{}','YYYY-MM-DD HH24:MI:SS'),NOW(),{})".format(transaction_id, customer_id, orderString,start_time,totalPrice))
        cursor.execute("DELETE FROM session WHERE transaction_id = {}".format(transaction_id))
        cursor.execute("DELETE FROM purchases WHERE transaction_id = {}".format(transaction_id))
        return True


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


def make_payment(customer_id, customer_token="tok_visa"):
    stripe.api_key = "sk_test_cH2UFk3P0H91hN1oTmo5HZhB"
    customer_price, _, _, _ = query_price(customer_id)
    token_visa = customer_token
    print('hi')
    try:
        charge = stripe.Charge.create(
            amount=int(100*customer_price),
            currency="usd",
            source="{}".format(token_visa),
            description="Test charge",
            transfer_group="placeholder_transfer"
        )
        exit_restaurant(customer_id)
        return "Payment Success", 200
    except:
        return "Payment Fail", 500

if __name__ == "__main__":
    # flush_database()
    #items are just random food_ids. can find on menuList.
    items = [103,106,303,202]
    items2 = [102,203,306]
    items3 = [100,101,303,301]
    items4 = [201,202,203]
    #enter_restaurant(customer_id,table_number,num_people)
    comments1 = ["hi","wat",None,"wat"]
    comments2 = ["hii", "watt", None, "watt"]
    comments3 = ["hiii", "wattt", None, "wattt"]
    comments4 = ["hiiii", "watttt", None, "wattt"]
    enter_restaurant(351,8,4)
    enter_restaurant(106,9,2)
    enter_restaurant(918,1,1)
    enter_restaurant(38150,8,9)
    # make_order(table_id,customer_id,items)
    make_order(351, items, comments1)
    make_order(106, items2,comments2)
    make_order(918, items3,comments3)
    make_order(38150, items4,comments4)
    edit_purchase(351,items[0],comments1[0],2.34)
    edit_purchase(106, items2[1], comments2[0], 3.45)
    edit_purchase(918, items3[0], comments3[0], 5.67)
    #query_price(table_id,customer_id)
    order_satisfied(351,103,"hi")
    order_satisfied(351, 202, "wat")

    print("Customer {}: Price is {} by ordering {} and staying for {} hours, with custom orders costing {}"
          .format(351, query_price(351)[0], query_price(351)[2],query_price(351)[1],query_price(351)[3]))
    print("Customer {}: Price is {} by ordering {} and staying for {} hours, with custom orders costing {}"
          .format(106, query_price(106)[0], query_price(106)[2],query_price(106)[1],query_price(106)[3]))
    print("Customer {}: Price is {} by ordering {} and staying for {} hours, with custom orders costing {}"
          .format(918, query_price(918)[0], query_price(918)[2],query_price(918)[1],query_price(918)[3]))
    print("Customer {}: Price is {} by ordering {} and staying for {} hours, with custom orders costing {}"
          .format(38150, query_price(38150)[0], query_price(38150)[2],query_price(38150)[1],query_price(38150)[3]))

    print(get_stats(38150))
    # exit_restaurant(351)
    # exit_restaurant(106)
    # exit_restaurant(918)
    # exit_restaurant(38150)