from app import user_collection
from utils import hashPass
from utils import JWT
import os

class User:
  def __init__(self, body, fileImg):
    self.teste = {'name': body.get('name', None), 
                  'nick': body.get('nick', None), 
                  'email': body.get('email'), 
                  'pass': hashPass.hash_pass(body.get('pass'))}
    self.fileImg = fileImg


  def insert_user(self):
    if not user_collection.find_one({'email': self.teste['email']}):
      user = user_collection.insert_one(self.teste)
      userId = user.inserted_id
      user = user_collection.update_one(filter={'_id': userId}, update={'$set': {'userImg': './uploads/' + str(userId) + '-' + self.fileImg.filename}})
      self.set_img(userId)
      return user
    else: 
      return False


  def set_img(self, userId): 
    uplaod_url = './uploads'
    os.makedirs(uplaod_url, exist_ok=True)
    self.fileImg.save(os.path.join(uplaod_url, str(userId) + '-' + self.fileImg.filename))


  def get_user(self):
    user = user_collection.find_one({"email": self.teste.get('email')})
    return user


  def login(self):
    user = self.get_user()

    if user:
      if hashPass.compare_hash(user['pass'], self.teste['pass']):
        user['_id'] = str(user['_id'])
        return {'status': 202, 'token': str(JWT.create_token(user))}
      else: 
        return {'status': 406, 'message': 'Senha incorreta'}
    else:
      return {'status': 406, 'message': 'Usuário não existente'}