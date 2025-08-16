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
  print(f"Mensaje from :{From}")
  print(f"Mensaje body : {Body}")
  print(f"Id del mensaje: {MessageSid}")
  print(f"NumMedia : {NumMedia}")

  try:
     
     respuesta_ia = openAIProcesso.create_analysis_prompt(Body)
     message_id = twilioService.send_message(respuesta_ia, From)
     #respuesta_ia = contestar_usuario(Body)
     #message_id= enviar_mensaje_whatsapp(respuesta_ia, From)
     print(f"Respuesta enviada : {message_id}")
     return {
        "status": "success",
        "message": "Mensaje procesado y respuesta enviada",
        "response_id": message_id
     }
  except Exception as e:
     print(f"Error procesando mensaje{e}")
     #error_mensaje = contestar_usuario(e)
     #enviar_mensaje_whatsapp(error_mensaje, From)
     return {"status":"error","message":str(e)}
  

if __name__ =="__main__":
   print("Iniciando whatsapp assistant...")
   #print(f"Twilio phone: {twilio_phone}")
   #print(f"Your phone numbre: {numero_destino}")
   uvicorn.run(app, host="0.0.0.0", port=8000)
