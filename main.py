from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3
import os
import csv
import json
import time

app = Flask(__name__)
app.secret_key = os.urandom(12)


DB_NAME = 'iiiteats.db'



def getUser():
    if not session.get('user'):
        return {'id': 0, 'name': 'Guest', 'phone': 0}
    user = session['user'] 
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM users WHERE rollno=?', (user,))
    user = myCursor.fetchone()
    myConn.close()
    
    usr = {}

    if user is not None :
        usr['id'] = user[0]
        usr['name'] = user[1]
        usr['phone'] = user[4]

    else:
        usr['id'] = 0
        usr['name'] = 'Guest'
        usr['phone'] = 9874563210
        
    return usr

@app.route('/')
def index():
    print(session)
    if session.get('user'):
        return render_template('index.html', noback = 1, user = getUser())
    else:
        return render_template('login.html', user= getUser())


@app.route('/login', methods=[ 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        register = request.form['register']
        print(request.form)

        myConn = sqlite3.connect(DB_NAME)
        myCursor = myConn.cursor()
        myCursor.execute('SELECT * FROM users WHERE email=? ', (email,))

        user = myCursor.fetchone()
        if user is not None:
            if user[3]==password:
                session['user'] = user[0]
                return render_template('index.html', noback = 1, user = getUser())
            else:
                return render_template('login.html', error = 'Invalid Password', email = email, user = getUser())
            
        else:
            if register == 'true':
                name = request.form['name']
                phone = int(request.form['phone'])
                rollno = int(request.form['rollno'])
                myCursor.execute('INSERT INTO users (rollno, name, phone, email, password) VALUES (?, ?, ?, ?, ?)', (rollno, name, phone, email, password))
                myConn.commit()
                custID = myCursor.lastrowid

                session['user'] = custID

                return redirect(url_for('index', noback = 1))
            return render_template('login.html', error = 'User not found. Please register.', register = 'true', email = email)
        
    else:
        return render_template('login.html')


CANTEEN_IMAGE_URL = "https://raw.githubusercontent.com/gaurav-behera/canteen-images/main/squareimages/"
CANTEEN_BANNER_URL = "https://raw.githubusercontent.com/gaurav-behera/canteen-images/main/canteenimages/"
ITEM_IMAGE_URL = "https://raw.githubusercontent.com/gaurav-behera/canteen-images/main/"

@app.route('/canteens')
def canteens():
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM canteens')
    canteens = myCursor.fetchall()

    cant = []
    for canteen in canteens:
        ct = {}
        ct['id'] = canteen[0]
        ct['name'] = canteen[1]
        ct['landmark'] = canteen[2]
        ct['desc'] = canteen[3]
        ct['img'] = CANTEEN_IMAGE_URL + str(canteen[0]) + '.jpg'
        cant.append(ct)

    return render_template('canteens.html', canteens = cant, user = getUser())

def getCanteenInfo(canteen_id):
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM canteens WHERE id=?', (canteen_id,))
    canteen = myCursor.fetchone()

    ct = {}
    ct['id'] = canteen[0]
    ct['name'] = canteen[1]
    ct['landmark'] = canteen[2]
    ct['desc'] = canteen[3]
    ct['img'] = CANTEEN_IMAGE_URL + str(canteen[0]) + '.jpg'

    return ct

def getCanteenItem( canteen_id):
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM items WHERE canteen_id=?', (canteen_id,))
    data = myCursor.fetchall()


    canteen = {}
    myCursor.execute('SELECT * FROM canteens WHERE id=?', (canteen_id,))
    canteen['id'], canteen['name'], canteen['landmark'], canteen['desc'] = myCursor.fetchone()

    canteen['img'] = CANTEEN_BANNER_URL + str(canteen['id']) + '.jpg'


    cats = []
    for rec in data:
        item = {}
        item['id'] = rec[0]
        item['name'] = rec[1]
        item['price'] = "₹ " + str(rec[2])
        item['img']= ITEM_IMAGE_URL + str(rec[0]) + '.jpg'
        item['non_veg'] = 1 if rec[4] else 0
        item['canteen_id'] = canteen_id

        if (rec[5]) not in [cat['name'] for cat in cats]:
            cats.append({'name': rec[5], 'items': []})
        
        for cat in cats:
            if cat['name'] == rec[5]:
                cat['items'].append(item)
                break
        

    canteen['categories'] = cats
    myConn.close()
    return canteen


def getCartItem():
    if session.get('cart'):
        cart = session['cart'].replace("'", '"')
    else:
        cart = "{}"

    return json.loads(cart)


@app.route('/canteen/<canteen_id>')
def canteen(canteen_id):
    canteen = getCanteenItem(canteen_id)

    filter = request.args.get('filter', 'all')
    # nv = request.args.get('nv' , '1')



    filt = []
    if filter == 'all':
        filt = [c['name'] for c in canteen['categories']]
    else:
        filt = filter.split(',')
    print(filt)

    return render_template('menu.html', canteen = canteen, cart = getCartItem(), user = getUser(), filter = filt)


# @app.route('/filterMenu', methods=['GET'])
# def filterMenu():
#     filt = filt.split(',')

#     return render_template('menu.html', canteen = canteen, cart = getCartItem(), user = getUser(), filter = filt)

@app.route('/addToCart', methods=['GET', 'POST'])
def cart():
    cart = getCartItem()

    item_id = int(request.args['item_id'])
    canteen_id = int(request.args['canteen_id'])
    quantity = int(request.args['quantity'])

    if cart.get('canteen_id', 0) != canteen_id:
        print('new canteen')
        cart['items'] = []
        cart['itemList'] = []

    else:
        cart['items'] = cart.get('items', [])
        cart['itemList'] = [item['id'] for item in cart['items']]

    cart['canteen_id'] = canteen_id

    for item in cart['items']:
        if item_id == item['id'] :
            if quantity == 0:
                cart['items'].remove(item)
                cart['itemList'].remove(item_id)
            else:
                item['quantity'] = quantity
            break
    else:
        cart['items'].append({'id': item_id, 'quantity': quantity})
        cart['itemList'].append(item_id)


    session['cart'] = json.dumps(cart)
    print(session['cart'])


    return render_template('menu.html', canteen = getCanteenItem, cart = cart, user = getUser())


@app.route('/checkout', methods=['POST'])
def checkout():

    item_id = int(request.args['item_id'])
    quantity = int(request.args['quantity'])

    cart = getCartItem()
    for item in cart['items']:
        if item_id == item['id'] :
            if quantity == 0:
                cart['items'].remove(item)
                cart['itemList'].remove(item_id)
            else:
                item['quantity'] = quantity
            break
    
    session['cart'] = json.dumps(cart)

    print(cart)
    # return "Success"
    return redirect(url_for('showCart'))


@app.route('/order/status/<order_id>', methods=['POST'])
def orderStatus(order_id):
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM liveorders WHERE id=?', (order_id,))
    rec = myCursor.fetchone()

    if rec is None:
        return redirect(url_for('home'))
    
    status = int(rec[3])

    obj = {}
    obj['state1'] = 0
    obj['state2'] = 0
    obj['state3'] = 0
    obj['state4'] = 0
    for i in range(1, status + 1):
        obj["state" + str(i)] = 1
    
    return obj
    

def getItem(itemID):
    myconn = sqlite3.connect(DB_NAME)
    myCursor = myconn.cursor()
    myCursor.execute('SELECT * FROM items WHERE id=?', (itemID,))
    rec = myCursor.fetchone()

    item = {}
    item['id'] = rec[0]
    item['name'] = rec[1]
    item['price'] = "₹ " + str(rec[2])
    item['canteen_id']= int(rec[3])
    item['non_veg'] = 1 if rec[4] else 0

    myconn.close()
    return item



def getOrder(orderID):
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM liveorders WHERE id=?', (orderID,))
    rec = myCursor.fetchone()

    order = {}
    order['customer_id'] = rec[1]
    order['order_id'] = rec[2]
    order['status'] = rec[3]
    
    myCursor.execute('SELECT * FROM orders WHERE id=?', (order['order_id'],))
    rec2 = myCursor.fetchone()
    
    if rec2 is None:
        rec2 = [0, 0, '{}',0, 0, 0, 0, 0, '',0]

    order['canteen_id'] = rec2[3]
    its = []
    for it in json.loads(rec2[2]):
        item = getItem(it['id'])
        its.append({'id': it['id'], 'quantity': it['quantity'], 'price': item['price'], 'name': item['name'], 'non_veg': item['non_veg']}) 
    order['items'] = json.dumps(its)

    order['amount'] = rec2[5]
    order['del_charges'] = rec2[6]
    order['total'] = rec2[7]
    order['address'] = rec2[8]

    myCursor.execute('SELECT * FROM canteens WHERE id=?', (order['canteen_id'],))
    rec3 = myCursor.fetchone()

    if rec3 is None:
        rec3 = [0, '', '', '']

    order['canteen_name'] = rec3[1]

    myCursor.execute('SELECT * FROM users WHERE rollno=?', (order['customer_id'],))
    rec4 = myCursor.fetchone()

    if rec4 is None:
        rec4 = ['Guest', '', '', '', '9874563210']

    order['customer_name'] = rec4[1]
    order['customer_phone'] = rec4[4]

    return order


@app.route('/order/<orderID>', methods=[ 'POST'])
def order(orderID):
    return json.dumps(getOrder(orderID))

def getItemInfo (item_id):
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM items WHERE id=?', (item_id,))
    item = myCursor.fetchone()

    return item



@app.route('/cart')
def showCart():
    data = getCartItem()
    # print("Data",data)
    try:
        canteen = getCanteenInfo(data['canteen_id'])
    except KeyError:
        return "<h1>Empty Cart</h1>"
    
    print(canteen)
    
    cart = {}
    cartItems = []
    cart['items'] = cartItems
    total = 0
    for item2 in data['items']:
        it = {}
        item = getItemInfo(item2['id'])
        print(item)
        it['id'] = item[0]
        it['name'] = item[1]
        it['price'] = "₹ "+ str(item[2])
        it['quantity'] = item2['quantity']
        it['img'] = ITEM_IMAGE_URL + str(item[0]) + '.jpg'
        # it['non_veg'] = 1 if item[4] else 0
        # it['total'] = item2['quantity'] * item[2]
        total += int(it['quantity']) * int(it['price'].replace("₹ ", '').strip())
        cartItems.append(it)

    cart['total'] = total
    cart['delivery'] = round(total * 0.1)
    cart['grandTotal'] = "₹ "+ str(total + cart['delivery'])
    cart['total'] = "₹ "+ str(total)
    cart['delivery'] = "₹ "+ str(round(total * 0.1))
    

    return render_template('cart.html', cart = cart, canteenName = canteen['name'], user = getUser())

@app.route('/placeOrder', methods=['POST'])
def placeOrder():
    data = getCartItem()
    print("Data",data)
    user = getUser()
    print("User",user)
    address = request.args['address']

    for item in data['items']:
        it={}
        it['id'] = int(item['id'])
        it['quantity'] = int(item['quantity'])
        it['price'] = int(getItemInfo(it['id'])[2])
        it['total'] = it['quantity'] * it['price']
        data['total'] = data.get('total', 0) + it['total']
    
    data['delivery'] = round(data['total'] * 0.1)
    data['grandTotal'] = data['total'] + data['delivery']
    data['address'] = address



    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('INSERT INTO orders (customer_id, canteen_id, items, order_time, amount, del_charges, total, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user['id'], data['canteen_id'], json.dumps(data['items']), int(time.time()*1000), data['total'], data['delivery'], data['grandTotal'], data['address']))
    myConn.commit()

    orderID = myCursor.lastrowid
    myCursor.execute('INSERT INTO liveorders (customer_id, order_id,  status) VALUES (?, ?, ?)', (user['id'], orderID, 0))


    myConn.commit()

    myConn.close()

    return "Order Placed"


@app.route('/viewOrders')
def viewOrders():
    user = getUser()
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM liveOrders WHERE customer_id=?', (user['id'],))
    data = myCursor.fetchall()

    print("LiveOrders",(data))
    orders = []
    for rec in data:
        orders.append(getOrder(rec[2]))
    
    print(orders)
    myConn.close()

    return render_template('order-tracking.html', orders = orders, user = getUser())



def viewLiveOrders():
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM liveOrders')
    data = myCursor.fetchall()
    details = []
    for item in data:
        obj = {}
        obj['id'] = int(item[0])
        obj['customer_id'] = int(item[1])
        obj['order_id'] = int(item[2])
        obj['status'] = int(item[3])
        if item[4] is None:
            obj['partner_id'] = 0
        else:
            obj['partner_id'] = int(item[4])
            
        details.append(obj)
    return details
    
    
@app.route('/viewDeliveries')
def viewDeliveries():
    liveOrders = viewLiveOrders()
    orders = []
    for i in liveOrders:
        order = getOrder(i['order_id'])
        order['id'] = i['id']
        order['status'] = i['status']
        order['partner_id'] = i['partner_id']

        orders.append(order)

    return render_template('delivery.html', deliveries = orders, user = getUser())
        

def getLiveOrder(orderID):
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM liveOrders WHERE order_id=?', (orderID,))
    rec = myCursor.fetchone()
    order = getOrder(rec[2])
    order['id'] = rec[0]
    order['status'] = rec[3]
    order['partner_id'] = rec[4]
    myConn.close()
    return order


@app.route('/viewOrder/<orderID>')
def viewOrder(orderID):
    order = getLiveOrder(orderID)
    return order

@app.route('/yourDeliveries', methods=['GET'])
def yourDeliveries():
    user = getUser()
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('SELECT * FROM liveOrders WHERE partner_id=?', (user['id'],))
    data = myCursor.fetchall()

    print("LiveOrders",(data))
    orders = []
    for rec in data:
        order = getOrder(rec[2])
        order['id'] = rec[0]
        order['status'] = rec[3]
        order['partner_id'] = rec[4]

        orders.append(order)
    
    print(orders)
    myConn.close()

    return render_template('delivery-details.html', orders = orders, user = getUser())

@app.route('/takeUpOrder/<orderID>', methods=['POST'])
def takeUpOrder(orderID):
    user = getUser()
    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('UPDATE liveOrders SET partner_id=?  WHERE order_id=?', (user['id'], orderID))
    myCursor.execute('UPDATE liveOrders SET status=? WHERE order_id=?', ( 1, orderID))
    myConn.commit()
    myConn.close()
    return "Order Taken"


@app.route('/tnc', methods=['GET'])
def tnc():
    return render_template('tnc.html')


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')


@app.route('//updateOrder', methods=['POST'])
def updateOrder():
    status = request.args['status']
    orderID = request.args['order_id']

    myConn = sqlite3.connect(DB_NAME)
    myCursor = myConn.cursor()
    myCursor.execute('UPDATE liveOrders SET status=? WHERE order_id=?', (status, orderID))
    myConn.commit()
    myConn.close()
    return "Order Updated"


@app.route('/logout', methods=['GET'])
def logout():
    return "<h1>Logout Page</h1>"

@app.route('/cookie', methods=['GET'])
def cookie():
    return render_template('cookie.html')

@app.route('/user', methods=['GET'])
def user():
    return getUser()


if __name__ == '__main__':
    app.run(debug=True)
