from connection_pool import ConnectionFromPool
import json

from databaseAccessMethods import *

def getMenu(tableNumber):
    restaurantName = "Crooked Cooks"
    restaurantImage = "https://i.imgur.com/XvlwlIn.jpg"

    with ConnectionFromPool() as cursor:
        cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'menu'");
        menuHeaders = cursor.fetchall()
        cursor.execute("SELECT * FROM menu")
        nonparsedArray = cursor.fetchall()

    finalString = jsonifyReply(menuHeaders,nonparsedArray)
    fullJSON = '{{"name":"{}","imagehyperlink":"{}","menu":[{}]}}'.format(restaurantName, restaurantImage, finalString)
    return fullJSON

def getOrders(customer_id=None):
    restaurantName = "Crooked Cooks"
    restaurantImage = "https://i.imgur.com/XvlwlIn.jpg"
    sqlCommand = "SELECT session.table_number,session.start_time," \
                 "menu.price, purchases.food_id,purchases.delivered,purchases.comments,purchases.additional_price FROM session" \
                 " INNER JOIN purchases ON purchases.transaction_id = session.transaction_id" \
                 " INNER JOIN menu ON purchases.food_id = menu.food_id "
    if(customer_id is not None):
        sqlCommand+="WHERE session.customer_id = {}".format(customer_id)

    # sqlCommand = "SELECT * FROM session"
    with ConnectionFromPool() as cursor:
        # cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'session'");
        menuHeaders = [("table_number","integer"),("start_time","timestamp without time zone"),("price","numeric(4,2)"),("food_id","integer"),("delivered","boolean"),("comments","text"),("additional_price","numeric(4,2)")]
        cursor.execute(sqlCommand)
        nonparsedArray = cursor.fetchall()
    finalString = '{{"orders":[{}]}}'.format(jsonifyReply(menuHeaders, nonparsedArray))
    return finalString

# def getSession(tableNumber):
#     restaurantName = "Crooked Cooks"
#     restaurantImage = "https://i.imgur.com/XvlwlIn.jpg"
#
#     with ConnectionFromPool() as cursor:
#         cursor.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'session'")
#         menuHeaders = cursor.fetchall()
#         # print(menuHeaders)
#         cursor.execute("SELECT * FROM session")
#         nonparsedArray = cursor.fetchall()
#
#     finalString = '{{"entries":[{}]}}'.format(jsonifyReply(menuHeaders,nonparsedArray))
#     return finalString



def jsonifyReply(headers,rowInformation):
    #Returns a string in {"abc":"def","efg":"hij",..},{"abc":"def","efg":"hij",..},... format

    #Presumes headers is in [(column_name,data_type),...] format
    #Presumes row information is in [(elem1, elem2,..n),...] format where n=number of columns

    infoArray = []
    for i in range(len(rowInformation)):
        elementInfo = "{"
        for j in range(len(headers)):
            #LEFT ELEMENT: Header will definitely be in string format
            elementInfo+='"'
            elementInfo+=headers[j][0]
            elementInfo+='"'

            elementInfo+=":"
            #RIGHT ELEMENT: Data may not necessarily be in string format.
            #May need to add apostrophes to the column information, if it is a STRING or a ENUM
            if(headers[j][1]=='text' or headers[j][1]=='USER-DEFINED' or 'timestamp' in headers[j][1]):
                elementInfo+='"'
            #True needs to be converted to true, same for False to false >.>
            if(headers[j][1]=='boolean'):
                elementInfo+=str(rowInformation[i][j]).lower()
            else:
                elementInfo += str(rowInformation[i][j])
            if (headers[j][1] == 'text' or headers[j][1] == 'USER-DEFINED' or 'timestamp' in headers[j][1]):
                elementInfo += '"'
            if(j!=len(headers)-1):
                elementInfo+=","
        elementInfo+="}"
        infoArray.append(elementInfo)
    finalReply = ",".join(element for element in infoArray)
    return finalReply

if __name__=="__main__":
    print(getMenu(49))
    # myNiceText = json.loads(getSession(49))
    # print(json.dumps(myNiceText, sort_keys=True,indent = 4, separators = (',', ': ')))