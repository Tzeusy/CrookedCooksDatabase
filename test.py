import psycopg2

a = 'a'

try:
    print(int(a))
except Exception as exception:
    print(exception.__class__.__name__)