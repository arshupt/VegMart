from flask import redirect, render_template, url_for, flash, request, session
from shop import app,db
from shop.products.models import Addproduct

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        qty = request.form.get('qty')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and qty and request.method == "POST":
            Dict = {'name':product.name, 'price':float(product.price), 'qty':qty, 'image':product.image_1}
            DictItems = {product_id: Dict}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)

            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal=0
    grandtotal=0    
    for key, product in session['Shoppingcart'].items():
        subtotal+= float(product['price']) * float(product['qty'])
        grandtotal = float("%.2f" %subtotal)
    return render_template('/products/carts.html',grandtotal=grandtotal)

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if request.method == "POST":
        qty = request.form.get('qty')
        try:
           session.modified = True
           for key, item in session['Shoppingcart'].items():
               if int(key) == code:
                   item['qty']=qty
                   return redirect(url_for('getCart')) 
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deletecart/<int:id>')
def deleteitem(id):
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
