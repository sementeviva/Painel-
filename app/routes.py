from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import db, Admin, Client, Flow, MessageHistory
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'admin_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            return redirect(url_for('main.dashboard'))
        flash('Credenciais inválidas')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('main.login'))
    clients = Client.query.count()
    messages = MessageHistory.query.count()
    flows = Flow.query.count()
    return render_template('dashboard.html', clients=clients, messages=messages, flows=flows)

@bp.route('/flows')
def flows():
    if 'admin_id' not in session:
        return redirect(url_for('main.login'))
    all_flows = Flow.query.all()
    return render_template('flows.html', flows=all_flows)

@bp.route('/clients')
def clients():
    if 'admin_id' not in session:
        return redirect(url_for('main.login'))
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)

@bp.route('/history')
def history():
    if 'admin_id' not in session:
        return redirect(url_for('main.login'))
    messages = MessageHistory.query.order_by(MessageHistory.timestamp.desc()).limit(100).all()
    return render_template('history.html', messages=messages)

@bp.route('/stats')
def stats():
    if 'admin_id' not in session:
        return redirect(url_for('main.login'))

    today = datetime.utcnow()
    last_7_days = today - timedelta(days=7)

    msg_stats = db.session.query(
        func.date(MessageHistory.timestamp).label('date'),
        func.count().label('count')
    ).filter(MessageHistory.timestamp >= last_7_days)
    msg_stats = msg_stats.group_by(func.date(MessageHistory.timestamp)).all()

    client_count = Client.query.count()
    active_clients = Client.query.filter_by(active=True).count()
    flow_usage = db.session.query(Flow.name, func.count(MessageHistory.id)) \
        .join(Client, Client.id == MessageHistory.client_id) \
        .group_by(Flow.name).all()

    return render_template(
        'stats.html',
        msg_stats=msg_stats,
        client_count=client_count,
        active_clients=active_clients,
        flow_usage=flow_usage
    )
