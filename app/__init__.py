from flask import Flask
from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy, BaseQuery

from config import config

moment = Moment()
# db = SQLAlchemy(query_class=BaseQuery)
# csrf = CSRFProtect()


def create_app(config_name):

    config_name = 'development'
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    # db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
