from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('routes.dashboard'))
        return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    return render_template('dashboard.html')

@routes.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('routes.login'))

# ROTA TEMPORÁRIA PARA CRIAR USUÁRIO "semente"
@routes.route('/criar_admin')
def criar_admin():
    if User.query.filter_by(username='semente').first():
        return 'Usuário já existe.'
    password_hash = generate_password_hash('semente')
    user = User(username='semente', password=password_hash)
    db.session.add(user)
    db.session.commit()
    return 'Usuário semente criado com sucesso!'
