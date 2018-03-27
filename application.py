from flask import Flask, render_template, request, abort
import flask
import psycopg2
import json
from initialize_session import flush_database
from pullMenu import *

from connection_pool import ConnectionFromPool
from databaseAccessMethods import *
# DatabaseAccessMethods are the VOID methods - that is, these methods take in parameters, and do not return values.
# DatabaseRequestMethods are the JSON-returning methods, which are used to provide output to the API.

import datetime

application = app = Flask(__name__)

# Server is hosted on http://crookedcooks.ap-southeast-1.elasticbeanstalk.com/
# Deploy updates by running "eb deploy" from CLI within venv


@app.route('/api/menu')
def menu():
    tablenumber = request.args.get('table_number')
    if 0 < int(tablenumber) < 100:
        fullJSON = getMenu(tablenumber)
        return fullJSON
    else:
        return render_template('404.html'), 404


@app.route('/api/make_order', methods=['GET', 'POST'])
# def makeorder(uuid):
#USE UUID FOR ACTUAL POST REQUESTS. IT'S LIKE THIS FOR DEBUGGING THE FUNCTIONALITY.
def makeorder():
    customer_id = request.args.get('plid')
    if flask.request.method == 'GET':
        # #TODO: Convert json's to a CUSTOMER ID, and an array of tuples with [(food_id, comment),(food_id,comment),...] as the items.
        # #placeholder
        # customerId = 351
        # jsonItems = [(103,"hello"),(203,"world"),(101,"interesting")]
        #
        # print("Customer {} making orders {}".format(customerId,jsonItems))
        # orders = [jsonItem[0] for jsonItem in jsonItems]
        # comments = [jsonItem[1] for jsonItem in jsonItems]
        # print("Orders: {}, comments: {}".format(orders,comments))
        # make_order(customer_id=customerId,items=orders,comments=comments)
        return "Supposed to be a POST request"
    else:
        content = request.json
        print(content["orders"])
        for element in content["orders"]:
            make_order(customer_id,[element["food_id"]],[element["comment"]])
        return "Orders made"

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

@app.route('/api/special_order')
def special_order():
    #Returns the orders of each unclosed transaction ID, and whether it has been fulfilled or not
    #//array_to_json(array_agg(session)),array_to_json(array_agg(menu))
    customer_id = request.args.get('plid')
    food_id = request.args.get('food_id')
    comment = request.args.get('comment')
    additional_price = request.args.get('additional_price')
    edit_purchase(customer_id,food_id,comment,additional_price)
    return "Success"

@app.route('/api/register')
#Sample:
# 10.12.79.231:4995/api/register?table_number=49&plid=91234567&numpeople=8
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
            print("Testing")
            #Not necessary for num people.
            if (enter_restaurant(customer_id=userid, table_number=tablenum, num_people=0) < 0):
                return "Invalid - entry for customer already exists in table"
            else:
                return "False"
        else:
            return "NIL"
    else:
        return "NIL"

@app.route('/api/queryprice')
def queryprice():
    customer_id = request.args.get('plid')
    totalPrice, timeSpent, orders, customPrice = query_price(customer_id)
    returnString = "Customer {} has spent {} hours and has orders {} accruing up a total cost of {}".format(customer_id,timeSpent,orders,totalPrice)
    return returnString,200

@app.route('/api/exit')
def exitrestaurant():
    customer_id = request.args.get('plid')
    print("Customer {} exiting restaurant".format(customer_id))
    exit_restaurant(customer_id)
    return ("Customer {} exited restaurant".format(customer_id)),200

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

if __name__=='__main__':
    print("Starting Server...")
    app.run(host='0.0.0.0')