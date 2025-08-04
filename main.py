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
    if not destinatario:
       destinatario=numero_destino
    
    message = client.messages.create(
        body="Hola mundo",
        from_=f"whatsapp:{twilio_phone}",
        to=f"whatsapp:{destinatario}",
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


@app.post("/webhook")
async def webhook_whatsapp(
    From: str= Form(...),
    Body: str= Form(...),
    
)

