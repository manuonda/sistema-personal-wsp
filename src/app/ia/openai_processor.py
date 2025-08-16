""" OpeanAI Processor  - Clase Principal para procesamiento 
   de mensajes"""


import datetime
import json 
import os
from typing import TypedDict, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

class OpenAIProcesso:
    """ Procesador principal de OpenAI para multiples 
        recordatorios 
    """
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key= os.environ.get("OPENAI_API_KEY"),
            temperature=0.3,
            max_tokens=500,
            timeout=30
        )
        # self.context_builder = ContextBuilder()
        # self.prompt_templates = PromptTemplates()
    
    def process_message(self, user_phone:str, message: str) -> Dict:
       """ Method principal - procesa mensaje y retorna respuesta
       
       """
       try:
        print(f"Procesando mensaje de {user_phone}: {message}")    
         
        #crear prompts 
        prompt = self.create_analysis_prompt(message)
         
        #Enviar a OpenAI
        # messages = [
        #    SystemMessage(content="Eres un asistente personal util y amigable"),
        #    HumanMessage(content=prompt)
        # ]
        response = self.llm.invoke([
            {"role":"user", "content": prompt} 
        ]) 
       
        return response

       except Exception as ex:
          print(f"Error : {ex}")

    
    def create_analysis_prompt(self, user_message: str) -> str:
        """
          Crea el prompt que le dice a OpenAI que hacer   
        """

        current_time = datetime.now()

        return f"""
        Eres un asistente personal que detecta tareas/recordatorios en mensajes.
        
        MENSAJE DEL USUARIO: "{user_message}"
        
        Analiza el mensaje y responde SOLO con JSON válido:
        
        {{
            "tipo_mensaje": "recordatorios|conversacion",
            "recordatorios": [
                {{
                    "titulo": "nombre de la tarea",
                    "fecha": "YYYY-MM-DD o null si no especifica",
                    "hora": "HH:MM o null si no especifica", 
                    "tipo": "cita|medicamento|tarea|pago",
                    "completo": true/false
                }}
            ],
            "respuesta": "respuesta natural para el usuario",
            "necesita_mas_info": true/false
        }}
        
        REGLAS:
        1. Si detectas múltiples tareas, sepáralas en el array "recordatorios"
        2. Convierte fechas naturales: "el martes" → próximo martes, "mañana" → mañana
        3. Si falta fecha/hora, pon null y marca necesita_mas_info: true
        4. "completo" = true si tiene título, fecha y hora. false si falta algo
        
        EJEMPLOS:
        
        "sacar turno para el papá a las 16:00 el martes, retirar medicamentos"
        → 2 recordatorios:
           1. titulo: "Sacar turno para papá", fecha: "2025-08-12", hora: "16:00", tipo: "cita", completo: true
           2. titulo: "Retirar medicamentos", fecha: null, hora: null, tipo: "medicamento", completo: false
        
        "hola cómo estás"
        → tipo_mensaje: "conversacion", recordatorios: []
        
        FECHA ACTUAL: {current_time.strftime("%Y-%m-%d %H:%M")}
        DÍA ACTUAL: {current_time.strftime("%A")}
        
        Responde SOLO el JSON, sin texto extra.
        """
    