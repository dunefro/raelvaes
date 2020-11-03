from flask import Flask
from flask import Flask , request
from flask_restful import Resource, Api , reqparse
from flask_jwt import JWT , jwt_required , current_identity
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)
# The secret key is to be initialized before the api object is created
app.secret_key = 'aR4QpGzGgHcY7haxHT9g89Puph3NgvNBBMBMnHEC'
api = Api(app)
salt = b'6o\x96h`\xdf\xf1\xecL2`\xcf=\xf0`\xcc'

from app.v1 import access
from app.v1 import health