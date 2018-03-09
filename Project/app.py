from flask import Flask, render_template, request, abort
import psycopg2
import json
from initialize_session import flush_database

app = Flask(__name__)

@app.route('/api/menu')
def menu():
    connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')
    with connection.cursor() as cursor:
        cursor.execute("SELECT array_to_json(array_agg(menu)) FROM menu")
        menuArray = cursor.fetchall()
    menuArray = menuArray[0][0]
    menuItems = []
    for item in menuArray:
        jsonString="'"+str(item['food_id'])+"':"+str(item)
        menuItems.append(jsonString)
    fullJSON = '{'
    fullJSON+=','.join(menuItem for menuItem in menuItems)
    fullJSON+='}'
    return fullJSON

@app.route('/api/make_order', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    return uuid

@app.route('/api/admin/newmenu',methods=['GET','POST'])
def adminMenu():
    admin_verifier = request.args.get('keycode')
    ourKeycode = '12345'
    print(admin_verifier)
    if(admin_verifier!=ourKeycode):
        return render_template('404.html'), 404
    else:
        new_menu = request.json
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