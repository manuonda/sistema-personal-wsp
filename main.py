import os
from dotenv import load_dotenv
from fastapi import FastAPI , Form , Request
from src.app import OpenAIProcesso, TwilioService
import uvicorn

load_dotenv()

app = FastAPI(title="WhatsApp Assistant")
twilioService = TwilioService()
openAIProcesso = OpenAIProcesso()

@app.post("/webhook")
async def recibir_mensaje(
    From: str = Form(...),
    Body: str = Form(default=""),
    MessageSid: str = Form(...),
    NumMedia: str = Form(default="0"),
    To: str = Form(default=""),
    AccountSid: str = Form(default="")
):
  """Webhook para recibir mensajes de Whatsapp"""
  print(f"Mensaje from: {From}")
  print(f"Mensaje body: {Body}")
  print(f"Id del mensaje: {MessageSid}")
  print(f"NumMedia: {NumMedia}")
  print(f"To: {To}")
  print(f"AccountSid: {AccountSid}")

  try:
     
     respuesta_ia = openAIProcesso.process_message(From, Body)
     print(f"respuesta_ia: {respuesta_ia}")
     message_id = twilioService.send_message(respuesta_ia, From)
     print(f"Respuesta enviada : {message_id}")
  except Exception as e:
     print(f"Error procesando mensaje{e}")
     return {"status":"error","message":str(e)}
  

if __name__ =="__main__":
   print("Iniciando whatsapp assistant...")
   uvicorn.run(app, host="0.0.0.0", port=8000)
