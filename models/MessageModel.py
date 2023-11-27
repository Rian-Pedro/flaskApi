from app import message_collection

from datetime import datetime

def organizaDate(dic):

  if 'hour' and 'date' in dic:
    teste = f"{dic['date']} {dic['hour']}"
    return datetime.strptime(teste, '%Y-%m-%d %H:%M:%S')
  else:
    return datetime.min



class Message:
  def __init__(self, body):
    self.body = body

  def create_message(self):
    message = message_collection.insert_one(self.body)

    for value in message:
      value['id'] = str(value['_id'])
      del value['_id']

    return message
    
  @staticmethod
  def get_messages(userId, friendId):
    
    messages_sended = message_collection.find({'sender': userId, 'recipient': friendId})
    messages_rec = message_collection.find({'sender': friendId, 'recipient': userId})


    sended = [{k: v for k, v in message.items()} for message in list(messages_sended)]
    rec = [{k: v for k, v in message.items()} for message in list(messages_rec)]

    for value in sended:
      value['id'] = str(value['_id'])
      del value['_id']

    for value in rec:
      value['id'] = str(value['_id'])
      del value['_id']

    result = [*sended, *rec]

    testres = sorted(result, key=organizaDate)

    return testres