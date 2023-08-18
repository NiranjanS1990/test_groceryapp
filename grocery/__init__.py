from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_restx import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.database.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config["UPLOADED_PHOTOS_DEST"] = "grocery/static/upload"
db = SQLAlchemy()
db.init_app(app)
api=Api(version='1.0',title='Grocery App CURD Operation Api',description='Performs CURD opertions on  Category & Product list of Grocery',prefix='/api')
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
