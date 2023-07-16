from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("WEBSITE_KEY")
socketio = SocketIO(app)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dump.db'

app.config['SQLALCHEMY_BINDS'] = {}


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)