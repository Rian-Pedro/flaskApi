import random
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv 

load_dotenv()

smtp_server = "smtp.gmail.com"
smtp_port = 587


def getRandomCode():
  lista = [random.randint(0,9) for _ in range(6)]
  newList = list(map(str, lista))
  return "".join(newList)

class EmailSender:
  
  @staticmethod
  def send(recipient):
    message = MIMEMultipart()

    message["From"] = os.environ.get("SENDEREMAIL")
    message["To"] = recipient
    message["Subject"] = "Código de verificação"

    code = getRandomCode()

    email_body = f"aqui esta o seu codigo para recuperação: {code}"

    message.attach(MIMEText(email_body, "plain"))

    try:
      server_smtp = smtplib.SMTP(smtp_server, smtp_port)
      server_smtp.starttls()

      server_smtp.login(os.environ.get("SENDEREMAIL"), os.environ.get("EMAILPASS"))

      server_smtp.sendmail(os.environ.get("SENDEREMAIL"), recipient, message.as_string())

      server_smtp.quit()

      print("email enviado com sucesso")
      return code
    
    except Exception as e:
      print(f"erro ao enviar email: {e}")
