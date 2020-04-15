from flask import redirect, render_template, url_for, flash, request, session
from flask_login import login_required,current_user,login_user, logout_user
from shop import app,db,photos,bcrypt,login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register
import secrets,os

@app.route('/customer/register',methods=['POST','GET'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data,username=form.username.data, email=form.email.data,
                   password=hash_password,contact=form.contact.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data}, Thank you for registering','success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are Logged in','success')
            return redirect(url_for('hom'))
        flash('Incorrect Email or Password','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html',form=form)