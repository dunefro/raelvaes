from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT , jwt_required

app = Flask(__name__)
api = Api(app)

from app.v1 import access
from app.v1 import admin_views