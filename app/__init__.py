from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'semente'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    # Criação automática do banco e do usuário padrão
    from app.models import User
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='semente').first():
            user = User(username='semente')
            user.set_password('semente')
            db.session.add(user)
            db.session.commit()
            print("Usuário 'semente' criado automaticamente.")

    return app
