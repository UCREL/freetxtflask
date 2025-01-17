from flask import Flask
from flask_cors import CORS
from flask import Flask, session
from flask_session import Session
import os
from datetime import timedelta
from .extensions import db
from .models import Feedback
from .utilits import clear_directories
from apscheduler.schedulers.background import BackgroundScheduler
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the current app directory
print(BASE_DIR)
def create_app(debug=True):
   
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Uploaded')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'feedback.db')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SESSION_TYPE'] = 'filesystem'  
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'myapp_'
    app.config['SESSION_FILE_DIR'] = UPLOAD_FOLDER
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)  # set session to expire in 120 minutes
    Session(app)
    CORS(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Set up a scheduler to clear directories every two days
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=clear_directories, trigger='interval', days=2)
    scheduler.start()
    from .Home import Home
    app.register_blueprint(Home, url_prefix = '/')
    
    from .Home import About
    app.register_blueprint(About)    
    

    from .Home import Userguide
    app.register_blueprint(Userguide)

    from .feedback import feedback_bp
    app.register_blueprint(feedback_bp)



    from .summary import fileanalysis_summary
    app.register_blueprint(fileanalysis_summary)

    from .File_analysis import FileAnalysis
    app.register_blueprint(FileAnalysis)
    return app
