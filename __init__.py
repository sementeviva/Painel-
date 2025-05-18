from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = None

db = SQLAlchemy()
migrate = None

def create_app():
    global app, migrate
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)

    from app import routes
    app.register_blueprint(routes.bp)

    return app
