from flask import Flask, render_template, request, abort
import flask
import psycopg2
import json
from initialize_session import flush_database

from connection_pool import ConnectionFromPool
from pullMenu import getMenu
from databaseAccessMethods import *
#DatabaseAccessMethods are the VOID methods - that is, these methods take in parameters, and do not return values.
#DatabaseRequestMethods are the JSON-returning methods, which are used to provide output to the API.

import datetime

app = Flask(__name__)

@app.route('/api/menu')
def menu():
    tablenumber = request.args.get('tablenumber')
    if(int(tablenumber)>0 and int(tablenumber)<50):
        fullJSON = getMenu(tablenumber)
        return fullJSON
    else:
        return render_template('404.html'), 404

@app.route('/api/make_order', methods=['GET', 'POST'])
# def makeorder(uuid):
#USE UUID FOR ACTUAL POST REQUESTS. IT'S LIKE THIS FOR DEBUGGING THE FUNCTIONALITY.
def makeorder():
    # content = request.json
    # print(content)
    print("test")
    if flask.request.method == 'GET':
        #TODO: Convert json's to a CUSTOMER ID, and an array of tuples with [(food_id, comment),(food_id,comment),...] as the items.
        #placeholder
        print("test")
        customerId = 75
        jsonItems = [(103,"hello"),(203,"world")]

        print("Customer {} making orders {}".format(customerId,jsonItems))
        orders = [jsonItem[0] for jsonItem in jsonItems]
        comments = [jsonItem[1] for jsonItem in jsonItems]
        make_order(customer_id=customerId,items=orders,comments=comments)
        return "Success"
    else:
        return "Fail"

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
        sqlCommand += "WHERE session.transaction_id = "+transacnum
    else:
        sqlCommand += "WHERE session.end_time IS null"

    restaurantName = "Crooked Cooks"
    connection = psycopg2.connect(database=restaurantName, user='postgres', password='1234', host='localhost')
    with connection.cursor() as cursor:
        cursor.execute(sqlCommand)
        menuArray = cursor.fetchall()

@app.route('/api/register')
def tableno():
    possible_parameters = ['table_number','plid','numpeople']
    parameter_existence = [elem in request.args for elem in possible_parameters]
    tablenum = request.args.get('table_number')
    userid = request.args.get('plid')
    num_people = request.args.get('numpeople')

    try:
        tablenum = int(tablenum)
        userid = int(userid)
        num_people = int(num_people)
    except ValueError:
        return ("Invalid parameters - was one of them a string?")
    except TypeError:
        pass

    if(all(parameter_existence)):
        print("Creating new entry with Table Number {}, UserID {}, Numpeople {}".format(tablenum, userid,num_people))
        enter_restaurant(customer_id=userid,table_number=tablenum,num_people=num_people)
        return "Entry created with number of people"

    elif(parameter_existence[0] and parameter_existence[1] and not parameter_existence[2]):
        if(tablenum>=0 and tablenum<50):
            return "Requesting number of people"
        elif(tablenum>=50 and tablenum<100):
            #Not necessary for num people.
            with ConnectionFromPool() as cursor:
                cursor.execute("INSERT INTO session(table_number,customer_id,start_time) "
                               "VALUES({},{},NOW())".format(tablenum, userid))
                transactionNumber = cursor.execute("SELECT transaction_id FROM session WHERE customer")
            return "Entry created without number of people"
        else:
            return "Invalid"
    else:
        return "Invalid"

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