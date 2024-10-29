from app.config.common import Flask, os
from app.db.conectiondb import getConnection
from app.views import login, logout, registerUser, forgotPassword


def create_app():
    app = Flask(__name__)

    getConnection()

    app.register_blueprint(login.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(registerUser.bp)
    app.register_blueprint(forgotPassword.bp)

    return app