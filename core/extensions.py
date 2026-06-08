from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
#from flask_login import LoginManager
#from flask_bcrypt import Bcrypt

# Agregar aquí cualquier otra extensión que quieras usar de forma global en tu aplicación, 
# como LoginManager, JWTManager, Cache, Flask-Login, Flask-Mail, etc.

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager() 
#login_manager = LoginManager()
#bcrypt = Bcrypt()
