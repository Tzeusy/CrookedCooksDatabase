import psycopg2

connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM menu")
    a = cursor.fetchall()
    print(a)
    # connection.commit()
    # print(a)