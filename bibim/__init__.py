from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_ckeditor import CKEditor

app = Flask(__name__)


app.config['SECRET_KEY'] = 'bb4ded0c9d76fd84f9d47254ecac2647'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'liammcl33@gmail.com'
app.config['MAIL_PASSWORD'] = 'wxdbkdnaiwiayopi'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrpyt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
ckeditor = CKEditor(app)


mail = Mail(app)


from bibim.users.routes import users
from bibim.posts.routes import posts
from bibim.main.routes import main
from bibim.materials.routes import materials
from bibim.meetings.routes import meetings
from bibim.marketplace.routes import marketplace
from bibim.errors.handlers import errors


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(materials)
app.register_blueprint(meetings)
app.register_blueprint(marketplace)
app.register_blueprint(errors)
