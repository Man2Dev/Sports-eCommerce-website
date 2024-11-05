import re
import os
from datetime import datetime
from sqlalchemy import desc
from flask import render_template, flash, redirect, url_for, request, session
from __init__ import  app, db, bcrypt
from database import Customer
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request, render_template, jsonify, send_file



@app.route("/", methods=['GET','POST'])
def index():
    return render_template('<h1>home</h1>')



@app.route("/log_in", methods=['GET','POST'])
def log_in():
    return render_template('<h1>login</h1>')

@app.route("/sign_in", methods=['GET','POST'])
def sign_up():
    return render_template('<h1>login</h1>')

@app.route("/sports", methods=['GET','POST'])
def sport_page():
    return render_template('<h1>login</h1>')


@app.route("/category", methods=['GET','POST'])
def category_page():
    return render_template('<h1>login</h1>')


@app.route("/card_page", methods=['GET','POST'])
def card_page():
    return render_template('<h1>login</h1>')

