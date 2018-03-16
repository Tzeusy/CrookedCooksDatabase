from flask import Flask, render_template, request, abort
import flask
import psycopg2
import json
from initialize_session import flush_database
from pullMenu import *

from connection_pool import ConnectionFromPool
from databaseAccessMethods import *
#DatabaseAccessMethods are the VOID methods - that is, these methods take in parameters, and do not return values.
#DatabaseRequestMethods are the JSON-returning methods, which are used to provide output to the API.

import datetime

app = Flask(__name__)

@app.route('/api/menu')
def menu():
    tablenumber = request.args.get('table_number')
    if(int(tablenumber)>0 and int(tablenumber)<100):
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
    customer_id = request.args.get('plid')
    print(customer_id)
    if(customer_id is not None):
        print("Customer id provided - giving his order")
        return getOrders(customer_id)
    else:
        print("Customer id not provided - giving all orders")
        return getOrders()
    #TODO: Convert the info to JSON of table numbers:[{item & quantity},{item & quantity},...]

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

    if tablenum<0 or tablenum>100:
        return "NIL"

    if(all(parameter_existence)):
        if(enter_restaurant(customer_id=userid,table_number=tablenum,num_people=num_people)<0):
            return "Invalid - entry for customer already exists in table"
        else:
            print(
                "Creating new entry with Table Number {}, UserID {}, Numpeople {}".format(tablenum, userid, num_people))
            return "Entry created with number of people"

    elif(parameter_existence[0] and parameter_existence[1] and not parameter_existence[2]):
        if(tablenum>=0 and tablenum<50):
            return "True"
        elif(tablenum>=50 and tablenum<100):
            #Not necessary for num people.
            if (enter_restaurant(customer_id=userid, table_number=tablenum, num_people=0) < 0):
                return "Invalid - entry for customer already exists in table"
            else:
                return "False"
        else:
            return "NIL"
    else:
        return "NIL"

# @app.route('/api/exit')
# def exitrestaurant():
#     customer_id = request.args.get('plid')
#     print("Customer {} exiting restaurant".format(customer_id))
#     exit_restaurant(customer_id)


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