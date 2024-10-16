from app.config.common import Flask
from app.db.conectiondb import getConnection
from app.views import login, logout, registerUser

def create_app():
    app = Flask(__name__)
    
    getConnection(app)

    app.register_blueprint(login.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(registerUser.bp)

    return app