from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///filesplitter.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set upload and download folders relative to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
    app.config['DOWNLOAD_FOLDER'] = os.path.join(project_root, 'downloads')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes import main
    from .auth import auth
    from .models import User
    from .utils import init_scheduler
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    # Initialize file cleanup scheduler
    scheduler = init_scheduler(app)
    
    return app