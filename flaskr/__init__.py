from flask import Flask, current_app
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from models import db


# Moved the models in a separate file and imported them before being able to run Migrate


def create_app(test_config=None):
    # create and configure the flaskr
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config())
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    app.db = db
    db.app = app
    db.init_app(app)
    app.migrate = Migrate(app, db)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # https://stackoverflow.com/questions/31226287/how-do-i-run-an-action-for-all-requests-in-flask
    @app.after_request
    def close_session(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,PUT,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        current_app.db.session.close()
        return response

    from routes.errors import default_handler
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.register_error_handler(Exception, default_handler)
    from routes.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from routes.accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp, url_prefix='/accounts')

    return app
