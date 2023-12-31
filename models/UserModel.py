from app import user_collection
from utils import hashPass
from utils import JWT
from bson import ObjectId
import os

class User:
  def __init__(self, body, fileImg):
    self.teste = {'name': body.get('name', None), 
                  'nick': body.get('nick', None), 
                  'email': body.get('email'), 
                  'pass': hashPass.hash_pass(body.get('pass')),
                  'contacts': []}
    self.fileImg = fileImg


  def insert_user(self):
    if not user_collection.find_one({'email': self.teste['email']}):
      user = user_collection.insert_one(self.teste)
      userId = user.inserted_id
      user = user_collection.update_one(filter={'_id': userId}, update={'$set': {'userImg': "{}/{}/".format(os.getcwd(), 'uploads') + str(userId) + '-' + self.fileImg.filename}})
      self.set_img(userId)
      return user
    else: 
      return False


  def set_img(self, userId): 
    uplaod_url = "{}/{}/".format(os.getcwd(), 'uploads')
    print(os.getcwd())
    os.makedirs(uplaod_url, exist_ok=True)
    self.fileImg.save(os.path.join(uplaod_url, str(userId) + '-' + self.fileImg.filename))


  @staticmethod
  def get_user(email, id):
    if id is None:
      print('aqui email')
      user = user_collection.find_one({"email": email})
      return user
    else:
      user = user_collection.find_one({"_id": ObjectId(id)})
      return user
  
  
  @staticmethod
  def insert_contact(email, id): 
    user = user_collection.find_one({"email": email})
    user_collection.update_one( 
      {"_id": ObjectId(id)}, 
      {
        '$push': {
          'contacts': {
            'name': user.get('name'), 
            'nick': user.get('nick'), 
            'email': user.get('email'), 
            'chat': []
          }
        }
      })


  def login(self):
    user = self.get_user(self.teste.get('email'), None)

    if user:
      if hashPass.compare_hash(user['pass'], self.teste['pass']):
        user['_id'] = str(user['_id'])
        return {'status': 202, 'token': str(JWT.create_token(user))}
      else: 
        return {'status': 406, 'message': 'Senha incorreta'}
    else:
      return {'status': 406, 'message': 'Usuário não existente'}
    

  @staticmethod
  def update_pass(newPass, userEmail):
    try:
      user_collection.update_one({"email": userEmail}, {'$set': {'pass': hashPass.hash_pass(newPass)}})
      return {"status": 200}
    except Exception as e:
      return {"status": 500, "message": "algo deu errado no servidor"}
    
  @staticmethod
  def delUser(userId):
    user_collection.delete_one({"_id": ObjectId(userId)})
    return "ok"