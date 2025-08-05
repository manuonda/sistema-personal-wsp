import os
from twilio.rest import Client
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from fastapi import FastAPI , Form , Request
import uvicorn

load_dotenv()

app = FastAPI(title="WhatsApp Assistant")

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)
twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")
numero_destino = os.environ.get("YOUR_WHATSAPP_NUMBER")

def enviar_mensaje_whatsapp(mensaje:str, destinatario: str = None):
    """ Funcion que permite enviar un mensaje al usuario """
    print(f"Destinatario: {destinatario}")
    if not destinatario:
       destinatario=f"whatsapp:{numero_destino}"
    
    message = client.messages.create(
        body={mensaje},
        from_=f"whatsapp:{twilio_phone}",
        to=destinatario,
    )
    return message.sid

def contestar_usuario(mensaje_usuario):
    """Funcion que permite contestar al usuario con IA"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.environ["OPENAI_API_KEY"]
    )
    messages = [
        SystemMessage(content="Eres un asistente personal util y amigable"),
        HumanMessage(content=mensaje_usuario)
    ]
    response = llm.invoke(messages)
    return response.content

@app.post("/webhook-debug")
async def debug_webhook(request: Request):
    """Endpoint para ver TODOS los campos que envía Twilio"""
    try:
        # Capturar todos los datos del formulario
        form_data = await request.form()
        
        print("🔍 TODOS LOS CAMPOS DE TWILIO:")
        print("=" * 50)
        for key, value in form_data.items():
            print(f"  {key}: {value}")
        print("=" * 50)
        
        # También capturar headers
        print("📋 HEADERS:")
        for key, value in request.headers.items():
            print(f"  {key}: {value}")
        
        return {"status": "debug_ok", "fields": dict(form_data)}
        
    except Exception as e:
        print(f"❌ Error en debug: {e}")
        return {"error": str(e)}

@app.post("/webhook")
async def recibir_mesnae(
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
     
     respuesta_ia = contestar_usuario(Body)
     message_id= enviar_mensaje_whatsapp(respuesta_ia, From)
     print(f"Respuesta enviada : {message_id}")
     return {
        "status": "success",
        "message": "Mensaje procesado y respuesta enviada",
        "response_id": message_id
     }
  except Exception as e:
     print(f"Error procesando mensaje{e}")
     error_mensaje = contestar_usuario(e)
     enviar_mensaje_whatsapp(error_mensaje, From)
     return {"status":"error","message":str(e)}
  

if __name__ =="__main__":
   print("Iniciando whatsapp assistant...")
   print(f"Twilio phone: {twilio_phone}")
   print(f"Your phone numbre: {numero_destino}")
   uvicorn.run(app, host="0.0.0.0", port=8000)
