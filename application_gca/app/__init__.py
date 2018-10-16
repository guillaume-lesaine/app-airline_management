from flask import Flask, render_template, request
from config import Config
from flask_bootstrap import Bootstrap
import yaml

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config.from_object(Config)

from app import routes
