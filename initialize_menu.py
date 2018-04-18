import psycopg2
from connection_pool import ConnectionFromPool
#One-off; use this template to initialize new menus

# connection = psycopg2.connect(database='Crooked Cooks', user='postgres', password='1234', host='localhost')
with ConnectionFromPool() as cursor:

    menuList = []
    # Mains
    menuList.append(('Main', 100, 'Cheesy Chicken Burger', 'Deep Fried Chicken Leg Patty with Nacho Cheese. ', 4.50,"$S*",'https://i.imgur.com/CGJm0D3.jpg',True))
    menuList.append(('Main', 101, 'Tonkatsu Pork Burger', 'Crispy Pork Loin, Sunny Side Egg, Garlic Mayo', 4.50,"$S*",'https://i.pinimg.com/originals/76/33/2e/76332e9e816d02e49b26034a8e918d4b.jpg',True))
    menuList.append(('Main', 102, 'Sausage In A Cup', 'Veal Bratwurst Sausage, Mash & Home Made Gravy', 3.50,"$S*",'https://i.imgur.com/Uxlbdnl.png',True))
    menuList.append(('Main', 103, 'Mac and Cheese', 'Macaroni, Bacon, and Poached Egg', 4.00,"$S*",'https://i.imgur.com/g2eV1a6.jpg',True))
    menuList.append(('Main', 104, 'Toast Breakfast', 'Toast, Veal Sausage, Bacon, Mushroom, Scrambled Eggs', 4.90,"$S*",'https://i.imgur.com/Q2xwatl.jpg',True))
    menuList.append(('Main', 105, 'Chicken Cutlet Aglio Olio', 'Deep Fried Chicken Leg Patty, Linguine Pasta, Chilli, and Garlic', 4.90,"$S*",'http://2.bp.blogspot.com/--X1dUvxFmOc/Tv3P7bqfvVI/AAAAAAAAFOs/a5JDuX-lxSw/s1600/DSC_7819.jpg',True))
    menuList.append(('Main', 106, 'Tonkatsu Pork Aglio Olio', 'Crispy Pork Loin, Linguine Pasta, Chilli, Garlic', 4.90,"$S*",'http://lh3.googleusercontent.com/WFXuQMGwkdiePcQHHPgL-fMMzjoKeb1N_vYt3Sds4C8T8jbpv7AojEhDoBuZwCWoI54j6EtP8f2MBam2ZZgEx6w=s800',True))
    # Vegetarian
    menuList.append(('Veg', 201, 'Meat Free Mac and Cheese', 'Mushroom, Macaroni, and Poached Egg',4.00,"$S*",'https://images-gmi-pmc.edge-generalmills.com/c41ffe09-8520-4d29-9b4d-c1d63da3fae6.jpg',True))
    menuList.append(('Veg', 202, 'Salted Egg Tofu Burger','Deep Fried Tofu, Salted Egg Sauce, and Mushroom',4.50,"$S*",'https://i.imgur.com/Msv42ri.jpg',True))
    menuList.append(('Veg', 203, 'Mushroom Carbonara','Shitake Mushroom, Linguine, and Cream Sauce', 4.90,"$S*",'http://s3.amazonaws.com/finecooking.s3.tauntonclud.com/app/uploads/2017/04/18170534/051121056-01-spaghetti-carbonara-recipe-thumb16x9.jpg',True))
    # Sides
    menuList.append(('Side', 301, 'Shoe String Fries (2 Pieces)','No Description',2.00,"$S*",'https://cdn.instructables.com/FSG/CVH1/IC7HLKPV/FSGCVH1IC7HLKPV.LARGE.jpg',True))
    menuList.append(('Side', 302, 'Chicken Wings (2 Pieces)','Marinated Deep Fried Wings',3.00,"$S*",'https://s-i.huffpost.com/gadgets/slideshows/334551/slide_334551_5874792_free.jpg',True))
    menuList.append(('Side', 303, 'Spam Fries','Spam, Topped with Local Red Sugar',3.00,"$S*",'https://i.imgur.com/enXw3u1.png',True))
    menuList.append(('Side', 304, 'Popcorn Chicken','Deep Fried Crispy Chicken with Garlic Mayo',4.00,"$S*",'https://i.imgur.com/wX9HkCz.png',True))
    menuList.append(('Side', 305, 'Chicken Floss Fries','Shoe String Fries, Chicken Floss, and Truffle Mayo',4.00,"$S*",'https://burpple-1.imgix.net/foods/533ad73339e351d90c81452124_original.?w=570&fit=crop&q=80',True))
    menuList.append(('Side', 306, 'Cheesy Fries','Shoe String Fries with Nacho Cheese',4.00,"$S*",'https://i.imgur.com/zdzTHHl.png',True))
    menuList.append(('Side', 307, 'Lok Lok Broccoli','Torched Broccoli, Sambal Chilli, and Potato Chips',4.00,"$S*",'https://burpple-1.imgix.net/foods/4ce1aa4585b9639114a1533907_original.?w=645&dpr=1&fit=crop&q=80',True))
    # Addon functionality from Special Requests

    cursor.execute('DROP TABLE IF EXISTS menu CASCADE')
    cursor.execute('DROP TYPE IF EXISTS category CASCADE')
    cursor.execute("CREATE TYPE category AS ENUM('Main','Side','Veg');")
    cursor.execute('CREATE TABLE menu (itemid SERIAL PRIMARY KEY, food_category category, food_id integer, name text, description text, price numeric(4,2),currency text,image_link text,is_available boolean)')

    for item in menuList:
        cursor.execute("INSERT INTO menu(food_category, food_id, name,description,price,currency,image_link,is_available) "
                       "VALUES('{}','{}','{}','{}',{},'{}','{}','{}')".format(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print("Menu successfully added!")