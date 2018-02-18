import psycopg2

#One-off; use this template to initialize new menus

connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')
cursor = connection.cursor()

menuList = []
#Mains
menuList.append(('Main', 100, 'Cheesy Chicken Burger', 'Deep Fried Chicken Leg Patty with Nacho Cheese', 4.50, 'NoPictureYet'))
menuList.append(('Main', 101, 'Tonkatsu Pork Burger', 'Crispy Pork Loin, Sunny Side Egg, Garlic Mayo', 4.50, 'NoPictureYet'))
menuList.append(('Main', 102, 'Sausage In A Cup', 'Veal Bratwurst Sausage, Mash & Home Made Gravy', 3.50, 'NoPictureYet'))
menuList.append(('Main', 103, 'Mac and Cheese', 'Macaroni, Bacon, and Poached Egg', 4.00, 'NoPictureYet'))
menuList.append(('Main', 104, 'Toast Breakfast', 'Toast, Veal Sausage, Bacon, Mushroom, Scrambled Eggs', 4.90, 'NoPictureYet'))
menuList.append(('Main', 105, 'Chicken Cutlet Aglio Olio', 'Deep Fried Chicken Leg Patty, Linguine Pasta, Chilli, and Garlic', 4.90, 'NoPictureYet'))
menuList.append(('Main', 106, 'Tonkatsu Pork Aglio Olio', 'Crispy Pork Loin, Linguine Pasta, Chilli, Garlic', 4.90, 'NoPictureYet'))
#Vegetarian
menuList.append(('Veg', 201, 'Meat Free Mac and Cheese', 'Mushroom, Macaroni, and Poached Egg',4.00,'NoPictureYet'))
menuList.append(('Veg', 202, 'Salted Egg Tofu Burger','Deep Fried Tofu, Salted Egg Sauce, and Mushroom',4.50,'NoPictureYet'))
menuList.append(('Veg', 203, 'Mushroom Carbonara','Shitake Mushroom, Linguine, and Cream Sauce', 4.90,'NoPictureYet'))
#Sides
menuList.append(('Side', 301, 'Shoe String Fries (2 Pieces)','No Description',2.00,'NoPictureYet'))
menuList.append(('Side', 302, 'Chicken Wings (2 Pieces)','Marinated Deep Fried Wings',3.00,'NoPictureYet'))
menuList.append(('Side', 303, 'Spam Fries','Spam, Topped with Local Red Sugar',3.00,'NoPictureYet'))
menuList.append(('Side', 304, 'Popcorn Chicken','Deep Fried Crispy Chicken with Garlic Mayo',4.00,'NoPictureYet'))
menuList.append(('Side', 305, 'Chicken Floss Fries','Shoe String Fries, Chicken Floss, and Truffle Mayo',4.00,'NoPictureYet'))
menuList.append(('Side', 306, 'Cheesy Fries','Shoe String Fries with Nacho Cheese',4.00,'NoPictureYet'))
menuList.append(('Side', 307, 'Lok Lok Broccoli','Torched Broccoli, Sambal Chilli, and Potato Chips',4.00,'NoPictureYet'))
#Addon functionality from Special Requests

cursor.execute('DROP TABLE IF EXISTS menu CASCADE')
cursor.execute('DROP TYPE IF EXISTS category CASCADE')
cursor.execute("CREATE TYPE category AS ENUM('Main','Side','Veg');")
cursor.execute('CREATE TABLE menu (itemid SERIAL PRIMARY KEY, food_category category, food_id integer, name text, description text, price numeric(4,2),image_link text)')

for item in menuList:
    print(item[1])
    cursor.execute("INSERT INTO menu(food_category, food_id, name,description,price,image_link) "
                   "VALUES('{}','{}','{}','{}',{},'{}')".format(item[0],item[1],item[2],item[3],item[4],item[5]))

connection.commit()
connection.close()