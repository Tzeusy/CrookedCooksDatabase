from flask import Flask, render_template, request
import flask
import stripe
from random import choice, randint, random
from string import ascii_lowercase
# from credentials import api_key

from databaseRequestMethods import *
from databaseAccessMethods import *
# DatabaseAccessMethods are the VOID methods - that is, these methods take in parameters, and do not return values.
# DatabaseRequestMethods are the JSON-returning methods, which are used to provide output to the API.

application = app = Flask(__name__)

# Server is hosted on http://crookedcooks.ap-southeast-1.elasticbeanstalk.com/
# Deploy updates by running "eb deploy" from CLI within venv


@app.route('/api/menu')
def menu():
    table_number = request.args.get('table_number')
    if 0 < int(table_number) < 100:
        full_json = getMenu(table_number)
        return full_json
    else:
        return render_template('404.html'), 404


@app.route('/api/make_order', methods=['GET', 'POST'])
def web_make_order():
    customer_id = int(request.args.get('plid'))
    if flask.request.method == 'GET':
        return "Supposed to be a POST request", 500
    else:
        content = request.json
        print(content["orders"])
        for element in content["orders"]:
            make_order(customer_id, [element["food_id"]], [element["comment"]])
        return "Orders made", 200


@app.route('/api/existing_orders')
def get_orders():
    # Returns the orders of each unclosed transaction ID, and whether it has been fulfilled or not
    # array_to_json(array_agg(session)),array_to_json(array_agg(menu))
    customer_id = int(request.args.get('plid'))
    if customer_id is not None:
        print("Customer id provided - giving his order")
        return getOrders(customer_id)
    else:
        print("Customer id not provided - giving all orders")
        return getOrders()


@app.route('/api/admin/special_order')
def special_order():
    # Returns the orders of each unclosed transaction ID, and whether it has been fulfilled or not
    # array_to_json(array_agg(session)),array_to_json(array_agg(menu))
    customer_id = int(request.args.get('plid'))
    food_id = request.args.get('food_id')
    comment = request.args.get('comment')
    additional_price = request.args.get('additional_price')
    if not (customer_id or food_id or comment or additional_price):
        return render_template('404.html'), 404
    else:
        edit_purchase(customer_id, food_id, comment, additional_price)
        return "Success", 200


@app.route('/api/register')
# Sample:
# 10.12.79.231:4995/api/register?table_number=49&plid=91234567&numpeople=8
def table_no():
    possible_parameters = ['table_number', 'plid', 'num_people']
    parameter_existence = [elem in request.args for elem in possible_parameters]
    table_number = request.args.get('table_number')
    userid = request.args.get('plid')
    num_people = request.args.get('num_people')

    try:
        table_number = int(table_number)
        userid = int(userid)
        num_people = int(num_people)
    except ValueError:
        return "Invalid parameters - was one of them a string?", 500
    except TypeError:
        pass

    if table_number < 0 or table_number > 100:
        return "NIL", 500

    if all(parameter_existence):
        if enter_restaurant(customer_id=userid, table_number=table_number, num_people=num_people) < 0:
            return "Invalid - entry for customer already exists in table"
        else:
            print(
                "Creating new entry with Table Number {}, UserID {}, Numpeople {}"
                .format(table_number, userid, num_people))
            return "Entry created with number of people"

    elif parameter_existence[0] and parameter_existence[1] and not parameter_existence[2]:
        if 0 <= table_number < 50:
            return "True", 200
        elif 50 <= table_number < 100:
            print("Testing")
            # Not necessary for num people.
            if enter_restaurant(customer_id=userid, table_number=table_number, num_people=0) < 0:
                return "Invalid - entry for customer already exists in table"
            else:
                return "False", 200
        else:
            return "NIL"
    else:
        return "NIL"


@app.route('/api/get_session', methods=['GET'])
def web_get_session():
    return get_session()


@app.route('/api/query_price')
def web_query_price():
    customer_id = int(request.args.get('plid'))
    total_price, time_spent, orders, custom_price = query_price(customer_id)
    # return_string = "Customer {} has spent {} hours and has orders {} accruing up a total cost of {}"\
    #     .format(customer_id, time_spent, orders, total_price)
    return_string = "{" + \
                    '"customer_id":{}, "hours":{}, "orders": {}, "time_price":{}, "total_price": {}'\
                    .format(customer_id,time_spent,orders,orders,total_price) + "}"
    return return_string, 200


@app.route('/api/make_payment', methods=['GET'])
def web_make_payment():
    # this is just a test api key - with a real key we'll be implementing obfuscating measures, as this is a public git repo
    # @github repo data scrapers: hellooo!
    customer_id = int(request.args.get('plid'))
    user_token = request.args.get('token_id')
    if not customer_id or not user_token:
        return "Insufficient parameters", 500

    # account_id = "acct_1CAqhiB8IfO1QxmY"
    token_visa = "tok_visa"
    if(make_payment(customer_id,user_token)):
        return "Payment Success", 200
    else:
        return "Payment Fail", 500


@app.route('/api/admin/set_availability', methods=['GET'])
def web_set_unavailable():
    food_id = request.args.get('food_id')
    bool = request.args.get('boolean')
    is_bool_valid = (bool=='true' or bool=='false')
    if not food_id or not bool or not is_bool_valid:
        return "Invalid parameters", 500
    if(set_availability(food_id,bool)):
        return "Payment Success", 200
    else:
        return "Payment Fail", 500


@app.route('/api/get_time_price', methods=['GET'])
def web_get_time_price():
    customer_id = int(request.args.get('plid'))
    table_number = int(request.args.get('table_number'))
    if not customer_id or not table_number:
        return "Invalid parameters", 500
    else:
        print(get_time_and_price(customer_id,table_number))
        return get_time_and_price(customer_id,table_number), 200


@app.route('/api/exit')
def web_exit_restaurant():
    customer_id = int(request.args.get('plid'))
    print("Customer {} exiting restaurant".format(customer_id))
    exit_restaurant(customer_id)
    return ("Customer {} exited restaurant".format(customer_id)), 200


# ADMIN METHODS
@app.route('/api/admin/new_menu', methods=['GET', 'POST'])
def admin_menu():
    admin_verifier = request.args.get('keycode')
    our_keycode = '12345'
    print(admin_verifier)
    if admin_verifier != our_keycode:
        return render_template('404.html'), 404
    else:
        new_menu = request.get_json()
        print("JSON Received")
        print(new_menu)
        return admin_verifier


# Unnecessary - session auto-empties now
@app.route('/api/admin/flush', methods=['GET'])
def admin_flush():
    admin_verifier = request.args.get('keycode')
    our_keycode = '12345'
    print(admin_verifier)
    if admin_verifier != our_keycode:
        return "Invalid Keycode", 500
    else:
        print("Flushing session and purchases")
        flush_database()
        return "Database flushed"


@app.route('/api/admin/set_delivered',methods=['GET'])
def web_set_delivered():
    customer_id = int(request.args.get('plid'))
    food_id = request.args.get('food_id')
    if not customer_id or not food_id:
        return "Insufficient parameters", 500
    success = set_delivered(customer_id,food_id)
    if success:
        return "Done!", 200
    else:
        return "Failed", 500


# TEST CASES
@app.route('/api/create_test_case', methods=['GET'])
def build_fake_customers():
    food_options = [100, 101, 102, 103, 104, 105, 106, 201, 202, 203, 301, 302, 303, 304, 305, 306, 307]
    customer_ids = [11111111, 22222222, 33333333, 44444444]
    purchased_items = [[], [], [], []]
    comments = [[], [], [], []]
    rand_str = lambda n: ''.join([choice(ascii_lowercase) for _ in range(n)])
    for i in range(4):
        num_orders = randint(1, 9)
        table_number = randint(1, 99)
        num_people = randint(1, 8)
        for j in range(num_orders):
            rand_item = randint(0, len(food_options) - 1)
            purchased_items[i].append(food_options[rand_item])
            comments[i].append(rand_str(6))

        enter_restaurant(customer_ids[i], table_number, num_people)
        make_order(customer_ids[i], purchased_items[i], comments[i])
    return "Success", 200


@app.route('/api/exit_test_case',methods=['GET'])
def exit_test_case():
    make_payment(11111111)
    make_payment(22222222)
    make_payment(33333333)
    make_payment(44444444)
    return "Customers 11111111, 22222222, 33333333, 44444444 exited", 200


if __name__ == '__main__':
    print("Starting Server...")
    app.run(host='0.0.0.0')
