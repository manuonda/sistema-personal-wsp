"""
Ejemplo de uso del sistema personal de WhatsApp
"""

import os
from dotenv import load_dotenv
from src.app import TwilioService, OpenAIProcesso

# Cargar variables de entorno
load_dotenv()

def main():
    """Función principal de ejemplo"""
    try:
        # Inicializar servicios
        twilio_service = TwilioService()
        openai_processor = OpenAIProcesso()
        
        print("✅ Servicios inicializados correctamente")
        print(f"📱 Twilio configurado para: {twilio_service.phone_number}")
        
        # Ejemplo de procesamiento de mensaje
        mensaje_usuario = "Recordarme llamar al doctor mañana a las 3 PM"
        
        # Procesar con OpenAI (aquí necesitarías implementar el método en tu clase)
        print(f"💬 Procesando mensaje: {mensaje_usuario}")
        
        # Enviar mensaje de confirmación
        numero_destino = twilio_service.numero_destino
        if numero_destino:
            respuesta = "✅ Recordatorio programado exitosamente"
            success = twilio_service.send_message(respuesta, numero_destino)
            
            if success:
                print("✅ Mensaje enviado correctamente")
            else:
                print("❌ Error al enviar mensaje")
        else:
            print("⚠️ No se encontró número de destino configurado")
            
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
