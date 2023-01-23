from app.main import blp 
from flask import Blueprint, abort, render_template, url_for, redirect


@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/findrecipe')
def find_recipe():
    # form for tags
    return render_template('findrecipe.html')

@blp.route('/myaccount')
def my_account():
    return render_template('myaccount.html')