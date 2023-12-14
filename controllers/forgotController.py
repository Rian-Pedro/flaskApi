from app import app
from flask import request, jsonify
from models import UserModel
from services import EmailSender

@app.route("/verifyUser", methods=["GET"])
def verifyUser():
  email = request.args.get('email')
  res = UserModel.User.get_user(email, None)

  code = EmailSender.EmailSender.send(email)

  if res is None:
    return jsonify({"status": 500, "message": "não foi encontrado este email"})
  else:
    return jsonify({"status": 200, "code": code})


@app.route("/changePass", methods=["POST"]) 
def changePass():
  newPass = request.get_json()["newPass"]
  userEmail = request.get_json()["userEmail"]

  res = UserModel.User.update_pass(newPass, userEmail)

  print(newPass, userEmail)
  return jsonify(res)