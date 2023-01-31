from app.main import blp 
from flask import abort, render_template, url_for, redirect
from flask_login import current_user


@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/myaccount')
def my_account():
    return render_template('myaccount.html',user=current_user)