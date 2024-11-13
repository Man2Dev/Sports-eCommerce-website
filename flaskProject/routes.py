import re
import os
from datetime import datetime

from sklearn.gaussian_process.kernels import Product
from sqlalchemy import desc
from functools import wraps
from flask import render_template, flash, redirect, url_for, request, session, make_response
from __init__ import  app, db, bcrypt
from forms import RegistrationForm, LoginForm, SellerRegistrationForm

from database import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request, render_template, jsonify, send_file



def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache


@app.before_request
def require_login():
    # Only apply to routes where user needs to be logged in
    if request.endpoint in ['dashboard', 'cart'] and not current_user.is_authenticated:
        return redirect(url_for('login'))


@app.route("/", methods=['GET','POST'])
def index():
    sport = Sport.query.all()
    sport_dict = {each_sport.name: each_sport.image_url for each_sport in sport}

    categorys = Category.query.all()
    categorys_dict = {category.name: category.image_url for category in categorys}

    products = Item.query.all()
    products_dict = {product.name: [product.price,Item_Images.query.filter_by(item_id=product.id).first().image_url] for product in products}
    return render_template('index.html', sports = sport_dict, categorys=categorys_dict, products = products_dict )


#redirect to the homepage
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # need to add validations on the email
        search_user_by_email = User.query.filter_by(email=form.email.data).first()
        search_user_by_phone = User.query.filter_by(phonenum=form.phonenum.data).first()
        if search_user_by_email  or search_user_by_phone:
            flash('User already exists!', 'error')
            return render_template('register.html', form=form, messages='user exists')

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # if(form.type.data == 'Seller'):
        #     user = Seller(name = form.name.data, surname=form.surname.data, email=form.email.data,
        #                   phonenum=form.phonenum.data, address=form.address.data,password=hashed_password)
        # else:
        cart = Cart()
        db.session.add(cart)
        db.session.commit()
        user = Customer(name=form.name.data, surname=form.surname.data, email=form.email.data,
                      phonenum=form.phonenum.data, address=form.address.data, password=hashed_password,
                        cart_id=cart.id)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account is created!", "success")
        return redirect(url_for("index"))              #UPDATE THE REDIRECTION
    return render_template('register.html', form=form)

@app.route("/dashboard", methods=['GET','POST'])
@nocache
@login_required
def dashboard():
    if current_user.type == 'seller':
        return render_template('dashboard.html')
    elif current_user.type == 'customer':
        return render_template('dashboardcustomer.html')
    else:
        form = SellerRegistrationForm()
        if form.validate_on_submit():
            # need to add validations on the email
            search_user_by_email = User.query.filter_by(email=form.email.data).first()
            search_user_by_phone = User.query.filter_by(phonenum=form.phonenum.data).first()
            if search_user_by_email or search_user_by_phone:
                flash('User already exists!', 'error')
                return render_template('register.html', form=form, messages='user exists')

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = Seller(name=form.name.data, surname=form.surname.data, email=form.email.data,
                                             phonenum=form.phonenum.data, address=form.address.data,password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"Seller account is created!", "success")
            return redirect(url_for("dashboard"))

        return render_template('superuserdashboard.html', form=form)



@app.route("/products", methods=['GET','POST'])
def products():
    return render_template('products.html')


@app.route("/cart", methods=['GET','POST'])
@nocache
@login_required
def cart():
    return render_template('cart.html')

@app.route('/sport/<sport>')
def sport(sport):
    url = Sport.query.filter_by(name=sport).first_or_404().image_url
    return render_template('sports.html', Ssport=sport, image = url)

@app.route('/category/<category>')
def category(category):
    link = Category.query.filter_by(name=category).first_or_404()
    return render_template('category.html', Category=link.name, image = link.image_url)

@app.route('/product/<product>')
def product(product):
    prod = Item.query.filter_by(name=product).first_or_404()
    images = Item_Images.query.filter_by(item_id=prod.id).first()
    category = Category.query.filter_by(id=prod.category).first_or_404().name
    return render_template('card.html', product=prod, images=images, category=category)



@app.route("/card_page", methods=['GET','POST'])
def card_page():
    return render_template('card.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



#the loging in drop the cache of the browser