import re
import os
from datetime import datetime
from sqlalchemy import desc
from flask import render_template, flash, redirect, url_for, request, session
from __init__ import  app, db, bcrypt
from forms import RegistrationForm, LoginForm

from database import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request, render_template, jsonify, send_file



@app.route("/", methods=['GET','POST'])
def index():
    return render_template('index.html')



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
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
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

        if(form.type.data == 'Seller'):
            user = Seller(name = form.name.data, surname=form.surname.data, email=form.email.data,
                          phonenum=form.phonenum.data, address=form.address.data,password=hashed_password)
        else:
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
def dashboard():
    return render_template('dashboard.html')


@app.route("/products", methods=['GET','POST'])
def products():
    return render_template('products.html')


@app.route("/cart", methods=['GET','POST'])
def cart():
    return render_template('cart.html')

@app.route('/category/<sport>')
def category(sport):
    return render_template('sports.html', Ssport=sport)



@app.route("/card_page", methods=['GET','POST'])
def card_page():
    return render_template('<h1>login</h1>')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))