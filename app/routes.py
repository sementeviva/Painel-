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
@bp.route('/estatisticas')
def estatisticas():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    total_usuarios = User.query.count()
    total_mensagens = Message.query.count()
    ultimo_login = db.session.query(User).order_by(User.last_login.desc()).first()

    return render_template('estatisticas.html',
                           total_usuarios=total_usuarios,
                           total_mensagens=total_mensagens,
                           ultimo_login=ultimo_login.last_login if ultimo_login else None)
