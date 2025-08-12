
from twilio.rest import Client
import os
from twilio.rest import Client


class TwilioService:

    def __init__(self):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
        self.numero_destino = os.environ.get("YOUR_WHATSAPP_NUMBER")
        if not all([account_sid, auth_token]):
          raise ValueError("Faltan las credenciasl de twilio")
       
        self.client = Client(account_sid, auth_token)

    
    def send_message(self, message:str, to_number:str) -> bool:
       """ Funcion que permite enviar un mensaje al usuario por wsp 
          Args: 
            message(str): Mensaje a enviar 
            to_number(str): Numero destino
          Returns: 
            bool: True si se envio correctamente
       """

       try:
          if not to_number.startswith("whatsapp"):
             to_number = f"whatsapp:{to_number}"

          message_obj = self.client.messages.create(
             body=message,
             from_=f"whatsapp:{self.phone_number}",
             to=to_number
          )
          
          print(f"Mensaje enviado {message_obj.sid}")
          
          return True
       except Exception as ex:
           print(f"Error enviando mensaje: {ex}")
       