from flask import Flask, render_template, request, abort
import psycopg2
import json
from initialize_session import flush_database
from connection_pool import ConnectionFromPool

app = Flask(__name__)

def getMenu(tablenumber):
    restaurantName = "Crooked Cooks"
    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT array_to_json(array_agg(menu)) FROM menu")
        menuArray = cursor.fetchall()
    menuArray = menuArray[0][0]
    menuItems = []
    for item in menuArray:
        jsonString = str(item)
        menuItems.append(jsonString)
    menuString = ','.join(menuItem for menuItem in menuItems)
    menuString = menuString.replace("'", '"')
    imageLink = "https://i.imgur.com/XvlwlIn.jpg"
    fullJSON = '{{"name":"{}","imagehyperlink":"{}","menu":[ {} ]}}'.format(restaurantName, imageLink, menuString)
    return fullJSON

@app.route('/api/menu')
def menu():
    tablenumber = request.args.get('tablenumber')
    if(int(tablenumber)>0 and int(tablenumber)<50):
        fullJSON = getMenu(tablenumber)
        return fullJSON
    else:
        return render_template('404.html'), 404

@app.route('/api/make_order', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print(content)
    return uuid

@app.route('/api/existing_orders')
def get_orders():
    #Returns the orders of each unclosed transaction ID, and whether it has been fulfilled or not
    #//array_to_json(array_agg(session)),array_to_json(array_agg(menu))
    sqlCommand = "SELECT * FROM session" \
                 "INNER JOIN purchases ON purchases.transaction_id = session.transaction_id" \
                 "INNER JOIN menu ON purchases.food_id = menu.food_id" \
                 "WHERE session.end_time IS null"
    transacnum = request.args.get('number')
    if(transacnum is not None):
        sqlCommand += "WHERE session.transaction_id = "+transacnnum
    else:
        sqlCommand += "WHERE session.end_time IS null"

    restaurantName = "Crooked Cooks"
    connection = psycopg2.connect(database=restaurantName, user='postgres', password='1234', host='localhost')
    with connection.cursor() as cursor:
        cursor.execute(sqlCommand)
        menuArray = cursor.fetchall()

@app.route('/api/tableno')
def tableno():
    tablenum = request.args.get('number')
    userid = request.args.get('plid')
    #TODO: Create entry in database with table number and user id at this timestamp
    #Return T,F, or N for needsNumPeople, noNeedNumPeople, or invalidTableNo. accordingly
    return 'Success'

@app.route('/api/numpeople')
def numpeople():
    tablenum = request.args.get('number')
    print(tablenum)
    userid = request.args.get('plid')
    #TODO: Access database, associate plid with existing Session, enter number of people into that session
    return 'Success'

#ADMIN METHODS
@app.route('/api/admin/newmenu',methods=['GET','POST'])
def adminMenu():
    admin_verifier = request.args.get('keycode')
    ourKeycode = '12345'
    print(admin_verifier)
    if(admin_verifier!=ourKeycode):
        return render_template('404.html'), 404
    else:
        new_menu = request.get_json()
        print("JSON Received")
        print(new_menu)
        return admin_verifier

@app.route('/api/admin/flush',methods=['GET'])
def adminFlush():
    admin_verifier = request.args.get('keycode')
    ourKeycode = '12345'
    print(admin_verifier)
    if(admin_verifier!=ourKeycode):
        return render_template('404.html'), 404
    else:
        print("Flushing session and purchases")
        flush_database()
        return "Database flushed"

app.run(host='0.0.0.0',port=4995)