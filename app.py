from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

client = MongoClient("mongodb+srv://admin:{}@talkhub.b0k5fuv.mongodb.net/?retryWrites=true&w=majority".format("xLR1bW5fL1Z8vogq"))
db = client.test

user_collection = db.users
contact_collection = db.contatcs
user_config_collection = db.userconfigs
message_collection = db.messages

posts = db.posts

from controllers import userController, forgotController
from models import UserModel