import sqlite3
import csv


DB_NAME = 'iiiteats.db'

def insertCanteens():
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()

    myCursor.execute('INSERT INTO canteens (name, landmark) VALUES (?, ?)', ('Vindhya Canteen (VC)', 'Near Vindhya block'))
    myCursor.execute('INSERT INTO canteens (name, landmark) VALUES (?, ?)', ('Basketball Canteen (BBC)', 'Behind Amphi'))
    myCursor.execute('INSERT INTO canteens (name, landmark) VALUES (?, ?)', ('Juice Canteen (JC)', 'Near Guest House'))
    myCursor.execute('INSERT INTO canteens (name, landmark) VALUES (?, ?)', ('Tantra', 'Near JC'))
    myCursor.execute('INSERT INTO canteens (name, landmark) VALUES (?, ?)', ('Davids', 'Near JC'))
    myCursor.execute('INSERT INTO canteens (name, landmark) VALUES (?, ?)', ('Roll House', 'Near JC'))
    myConn.commit()

    jc = "JC is best known for its oreo shake, but its timeless watermelon with extra ice, seasonal and luxurious avocado honey shake and all-time favourite nimbu soda are iconic."
    rh = "Frankie's roll stall has the most descriptive canteen name on campus. It is exactly what it proclaims to be - a roll stall. You name it, it's there (as long as 'it' is paneer or chicken)"
    tn ="Tantra is the place where people go to make up for missed meals (this is getting cliché, but again, much more common than you think). It's the only place which sells meal-sized portions, but its menu has some interesting typos - 'chicken moms' among them."
    dv ="David's Bakery has the most reasonable timings of all the canteens on campus. Although slightly overpriced, their ice cream brownie is worth having. It's also the only place open past 2 AM."
    vc = "VC serves a wide variety of food items. Most popular among them include tea, coffee, puffs, omelettes, and sandwiches. However, known to very few, there are other items not mentioned on the menu which this canteen offers. These include pav bhaji and papdi chaat."
    bb = "BBC Maggi and Dosa are known campus-wide. This may seem like less variety to you, but the sheer number of permutations and combinations within these to tap into will ensure that you're never bored."
    myCursor.execute('UPDATE canteens SET description = ? WHERE id = ?', (vc, 1))
    myCursor.execute('UPDATE canteens SET description = ? WHERE id = ?', (bb, 2))
    myCursor.execute('UPDATE canteens SET description = ? WHERE id = ?', (jc, 3))
    myCursor.execute('UPDATE canteens SET description = ? WHERE id = ?', (tn, 4))
    myCursor.execute('UPDATE canteens SET description = ? WHERE id = ?', (dv, 5))
    myCursor.execute('UPDATE canteens SET description = ? WHERE id = ?', (rh, 6))
    myConn.commit()

    myConn.close()


def insertItems():
    f = open('menu.csv', 'r')
    reader = csv.reader(f)
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()

    for record in reader:
        nonveg = 1 if record[3]=='N' else 0
        myCursor.execute('INSERT INTO items (name, price, canteen_id, non_veg, category) VALUES (?, ?, ?, ?, ?)', (record[0], int(record[1]), int(record[2]), nonveg, record[4]))
    myConn.commit()
    myConn.close()



def initDB():
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('CREATE TABLE IF NOT EXISTS users (rollno INTEGER PRIMARY KEY NOT NULL, name TEXT, email TEXT, password TEXT, phone INTEGER)')
    myCursor.execute('CREATE TABLE IF NOT EXISTS canteens (id INTEGER PRIMARY KEY NOT NULL, name TEXT, landmark TEXT, description TEXT)')
    myCursor.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY NOT NULL, name TEXT, price INTEGER, canteen_id INTEGER, non_veg INTEGER, category TEXT, FOREIGN KEY(canteen_id) REFERENCES canteen(id))')
    # myCursor.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER, items TEXT, FOREIGN KEY(user_id) REFERENCES users(rollno))')
    myCursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY NOT NULL, customer_id INTEGER, items TEXT, canteen_id INTEGER, order_time INTEGER, amount INTEGER, del_charges INTEGER, total INTEGER, address TEXT, fulfilled INTEGER, FOREIGN KEY(customer_id) REFERENCES users(rollno), FOREIGN KEY(canteen_id) REFERENCES canteen(id))')
    myCursor.execute('CREATE TABLE IF NOT EXISTS liveOrders (id INTEGER PRIMARY KEY NOT NULL, customer_id INTEGER, order_id INTEGER, status INTEGER, partner_id INTEGER, FOREIGN KEY(customer_id) REFERENCES users(rollno), FOREIGN KEY(partner_id) REFERENCES users(rollno), FOREIGN KEY(order_id) REFERENCES orders(id))')
    myConn.commit()



    myConn.close()




initDB()
insertCanteens()
insertItems()
