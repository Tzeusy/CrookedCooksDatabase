import psycopg2
from connection_pool import ConnectionFromPool
#One-off; use this template to initialize new menus

# connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')
with ConnectionFromPool() as cursor:
#TODO: JSON to menuList converter

    menuList = []
    #Mains
    menuList.append(('Main', 100, 'Cheesy Chicken Burger', 'Deep Fried Chicken Leg Patty with Nacho Cheese. This item is incredibly delicious and you should totally purchase it. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum', 4.50,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Main', 101, 'Tonkatsu Pork Burger', 'Crispy Pork Loin, Sunny Side Egg, Garlic Mayo', 4.50,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Main', 102, 'Sausage In A Cup', 'Veal Bratwurst Sausage, Mash & Home Made Gravy', 3.50,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Main', 103, 'Mac and Cheese', 'Macaroni, Bacon, and Poached Egg', 4.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Main', 104, 'Toast Breakfast', 'Toast, Veal Sausage, Bacon, Mushroom, Scrambled Eggs', 4.90,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Main', 105, 'Chicken Cutlet Aglio Olio', 'Deep Fried Chicken Leg Patty, Linguine Pasta, Chilli, and Garlic', 4.90,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Main', 106, 'Tonkatsu Pork Aglio Olio', 'Crispy Pork Loin, Linguine Pasta, Chilli, Garlic', 4.90,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    #Vegetarian
    menuList.append(('Veg', 201, 'Meat Free Mac and Cheese', 'Mushroom, Macaroni, and Poached Egg',4.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Veg', 202, 'Salted Egg Tofu Burger','Deep Fried Tofu, Salted Egg Sauce, and Mushroom',4.50,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Veg', 203, 'Mushroom Carbonara','Shitake Mushroom, Linguine, and Cream Sauce', 4.90,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    #Sides
    menuList.append(('Side', 301, 'Shoe String Fries (2 Pieces)','No Description',2.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Side', 302, 'Chicken Wings (2 Pieces)','Marinated Deep Fried Wings',3.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Side', 303, 'Spam Fries','Spam, Topped with Local Red Sugar',3.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Side', 304, 'Popcorn Chicken','Deep Fried Crispy Chicken with Garlic Mayo',4.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Side', 305, 'Chicken Floss Fries','Shoe String Fries, Chicken Floss, and Truffle Mayo',4.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Side', 306, 'Cheesy Fries','Shoe String Fries with Nacho Cheese',4.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    menuList.append(('Side', 307, 'Lok Lok Broccoli','Torched Broccoli, Sambal Chilli, and Potato Chips',4.00,"$S*",'https://i.imgur.com/XvlwlIn.jpg',True))
    #Addon functionality from Special Requests

    cursor.execute('DROP TABLE IF EXISTS menu CASCADE')
    cursor.execute('DROP TYPE IF EXISTS category CASCADE')
    cursor.execute("CREATE TYPE category AS ENUM('Main','Side','Veg');")
    cursor.execute('CREATE TABLE menu (itemid SERIAL PRIMARY KEY, food_category category, food_id integer, name text, description text, price numeric(4,2),currency text,image_link text,is_available boolean)')

    for item in menuList:
        cursor.execute("INSERT INTO menu(food_category, food_id, name,description,price,currency,image_link,is_available) "
                       "VALUES('{}','{}','{}','{}',{},'{}','{}','{}')".format(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print("Menu successfully added!")