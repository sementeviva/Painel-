from flask import Blueprint, render_template, request, redirect, url_for
from app.models import User
from app import db

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
