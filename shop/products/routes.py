from flask import redirect, render_template, url_for, flash, request, session
from shop import app,db,photos
from .forms import Addproducts
from .models import Addproduct
from flask_login import login_required, current_user
import secrets,os

@app.route('/customer')
@login_required
def hom():
    products=Addproduct.query.filter(Addproduct.stock>0)
    return render_template('/products/index.html',products=products)

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product)

    
@app.route('/addproduct',methods=['POST','GET'])
def addproduct():
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        
        stock = form.stock.data
        desc = form.description.data
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, stock=stock, desc=desc, image_1=image_1, image_2=image_2,image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'The vegetable {name} has been added to your database','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html',title="Add Product Page",form=form)

@app.route('/updateproduct/<int:id>', methods=['POST','GET'])
def updateproduct(id):
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.desc = form.description.data 
        db.session.commit()
        flash(f'Product Updated','success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.description.data = product.desc
    return render_template('/products/updateproduct.html',form=form, product=product)