from connection_pool import ConnectionFromPool

#This is only necessary to clean out test cases. In production, these methods will NEVER be used.
#Session and purchases are self-cleaning in nature. When transaction IDs are complete, they automatically self-delete
#History stores a record of all past transactions.

def createEmptySession():
    with ConnectionFromPool() as cursor:
        cursor.execute('DROP TABLE IF EXISTS session CASCADE')
        cursor.execute('CREATE TABLE session (default_id SERIAL PRIMARY KEY, transaction_id integer, table_number integer, customer_id integer, num_people integer, start_time timestamp)')
    print("Session reset!")

def createEmptyPurchases():
    with ConnectionFromPool() as cursor:
        cursor.execute('DROP TABLE IF EXISTS purchases CASCADE')
        cursor.execute('CREATE TABLE purchases (transaction_id integer NOT NULL, food_id integer NOT NULL, delivered boolean, comments text)')

def createHistory():
    with ConnectionFromPool() as cursor:
        cursor.execute('DROP TABLE IF EXISTS history CASCADE')
        cursor.execute('CREATE TABLE history (default_id SERIAL PRIMARY KEY, transaction_id integer NOT NULL, '
                       'food_orders text[], start_time timestamp, end_time timestamp, total_price float)')
    print("History reset!")

def flush_database():
    createEmptyPurchases()
    createEmptySession()
    # createHistory()

if __name__ == "__main__":
    flush_database()