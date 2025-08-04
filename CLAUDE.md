# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Sistema personal de WhatsApp integrado con Twilio API. Proyecto en Python para automatización de mensajería.

## Project Structure
- `__main__.py` - Punto de entrada principal del proyecto
- Proyecto en fase inicial de desarrollo

## Development Setup
```bash
# Instalar dependencias (cuando se creen)
pip install -r requirements.txt

# Ejecutar la aplicación
python __main__.py
```

## Dependencies Expected
- `twilio` - SDK oficial de Twilio para Python
- `python-dotenv` - Para manejo de variables de entorno
- `flask` o `fastapi` - Para webhooks (si se necesita)

## Environment Variables
Las credenciales de Twilio deben configurarse en `.env`:
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_PHONE_NUMBER

## Development Guidelines
- Este es un proyecto personal en desarrollo inicial
- El desarrollador prefiere trabajar como senior-junior, siendo guiado sin modificaciones automáticas del código
- Sugerir mejores prácticas y arquitectura, pero no implementar sin solicitud explícita
- Enfoque en integración con WhatsApp Business API a través de Twilio

## Common Commands
```bash
# Ejecutar el proyecto
python __main__.py

# Instalar Twilio SDK
pip install twilio python-dotenv

# Verificar sintaxis
python -m py_compile __main__.py
```