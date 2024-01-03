from app import user_collection, contact_collection, message_collection
import os

def clean():
  pasta =  f"{os.getcwd()}/uploads"
  arquivos = os.listdir(pasta)

  for arq in arquivos:
    
    full_path = os.path.join(pasta, arq)

    user_collection.find({}) and user_collection.delete_many({})
    contact_collection.find({}) and contact_collection.delete_many({})
    message_collection.find({}) and message_collection.delete_many({})

    if os.path.isfile(full_path):
      os.remove(full_path)
      print(f"arquivo {full_path} removido com sucesso")
