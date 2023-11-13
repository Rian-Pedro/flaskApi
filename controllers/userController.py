from app import app
from flask import request, jsonify, g, send_file
from models import UserModel
from utils import JWT

import os

# Request token JWT
@app.after_request
def after(response):
    path = request.path
    method = request.method

    if path == '/user' and method == 'GET':
        body = request.args.to_dict()

        if 'token' in body:
            decode_token = JWT.decode_token(body.get('token'))

            if not decode_token:
                return jsonify({"status": 406, "message": 'Token expirado'})
            else:
                return jsonify({'status': 202, 'token': body.get('token')})
            
        else: 
            return response
    
    return response

# Register User
@app.route("/user", methods=['POST'])
def userPost():
    data = {'name': request.form['name'], 
            'nick': request.form['nick'],
            'email': request.form['email'],
            'pass': request.form['pass']}

    file = request.files['img']
    newUser = UserModel.User(data, file)
    status = newUser.insert_user()

    if not status:
        return jsonify({'status': 406, 'message': 'E-mail já existente'})

    return jsonify({'status': 200})


# Login User
@app.route("/user", methods=['GET'])
def userGet():
   user = request.args.to_dict()
   res = UserModel.User(user, None).login()
   
   if res['status'] == 202:
       return jsonify(res)
   else: 
       return jsonify(res)
   

@app.route('/getImg', methods=['GET'])
def getImg():
    return send_file(path_or_file=request.args.get('src'))