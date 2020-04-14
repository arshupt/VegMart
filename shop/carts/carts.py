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
            Dict = {'name':product.name, 'price':int(product.price), 'qty':qty, 'image':product.image_1}
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
