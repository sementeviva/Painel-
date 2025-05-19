from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import User
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha inválidos', 'danger')
    return render_template('login.html')

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('dashboard.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login'))
