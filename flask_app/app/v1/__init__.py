from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

from app.v1 import views
from app.v1 import admin_views