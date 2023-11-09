import hashlib

def hash_pass(password):
  sha256 = hashlib.sha256()
  password_bytes = password.encode('utf-8')
  salt = "minhaSaltAleatoria".encode('utf-8')
  sha256.update(password_bytes + salt)
  hashed_password = sha256.hexdigest()
  return hashed_password

def compare_hash(BD_password, user_password):
  if user_password == BD_password:
    return True
  else:
    return False