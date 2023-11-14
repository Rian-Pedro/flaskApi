from app import contact_collection

class Contact:
  def __init__(self, body):
    self.userId = body.get('userId')
    self.contactId = body.get('contactId')

  def insert_contact(self):
    user = contact_collection.insert_one({'userId': self.userId, 
                                          'contactId': str(self.contactId)})
    
  @staticmethod
  def getAllContacts(userId):
    contactList = contact_collection.find({'userId': userId})
    print(contactList)