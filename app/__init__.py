from flask import Flask
from flask_bootstrap import Bootstrap
import secrets

def create_app():
    app = Flask(__name__, static_folder='../static')  # Specify static folder location
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    Bootstrap(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
