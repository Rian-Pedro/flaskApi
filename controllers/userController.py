from app import app
from flask import request, jsonify, g, send_file
from bson import json_util
from models import UserModel, ContactModel, MessageModel
from utils import JWT
import json

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


# Pegar usuário
@app.route("/getUser", methods=['GET'])
def getUser():
    contactEmail = request.args.to_dict()
    print(request.args.to_dict())

    if 'email' in contactEmail and contactEmail['email']:
        contact = UserModel.User.get_user(contactEmail['email'], None)
    elif 'contactId' in contactEmail and contactEmail['contactId']:
        contact = UserModel.User.get_user(None, contactEmail['contactId'])

    if contact is not None:
        return jsonify({
            'name': contact.get('name'),
            'nick': contact.get('nick'),
            'userImg': contact.get('userImg'),
            'id': str(contact.get('_id'))
        })
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404


# Criar contato
@app.route("/newContact", methods=['POST'])
def newContact():
    data = request.get_json()
    contactModel = ContactModel.Contact({'userId': data.get('userId'), 
                                         'contactId': data.get('contactId')})
    contactModel.insert_contact()
    
    return jsonify({'status': 202})
   

# Pegar Imagem
@app.route('/getImg', methods=['GET'])
def getImg():
    return send_file(path_or_file=request.args.get('src'))


@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    userId = request.args.to_dict().get('userId')
    
    teste = ContactModel.Contact.getAllContacts(userId)
    lista = []
    
    for t in teste:
        t['_id'] = str(t['_id'])
        lista.append(t)

    return jsonify(lista)

@app.route('/getMessages', methods=['GET'])
def getMessages():
    
    userId = request.args.to_dict().get('userId')
    friendId = request.args.to_dict().get('friendId')

    result = MessageModel.Message.get_messages(userId, friendId)

    return jsonify(result)