from connection_pool import ConnectionFromPool

#Intended to run at the start of every day or week or something; just to flush the session clean

def createEmptySession():
    with ConnectionFromPool() as cursor:
        cursor.execute('DROP TABLE IF EXISTS session CASCADE')
        cursor.execute('CREATE TABLE session (transaction_id SERIAL PRIMARY KEY, table_number integer, customer_id integer, num_people integer, start_time timestamp, end_time timestamp)')

def createEmptyPurchases():
    with ConnectionFromPool() as cursor:
        cursor.execute('DROP TABLE IF EXISTS purchases CASCADE')
        cursor.execute('CREATE TABLE purchases (transaction_id integer NOT NULL, food_id integer NOT NULL, delivered boolean)')

def flush_database():
    createEmptyPurchases()
    createEmptySession()

if __name__ == "__main__":
    flush_database()