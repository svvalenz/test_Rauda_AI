import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI

def load_config():
    """Carga las variables de entorno"""
    load_dotenv()
    return {
        'api_key': os.getenv('OPENAI_API_KEY'),
        'model_name': os.getenv('MODEL_NAME')
    }

def read_tickets(file_path):
    """Lee el archivo CSV de tickets"""
    try:
        return pd.read_csv(file_path, sep=';')
    except Exception as e:
        raise Exception(f"Error al leer el archivo CSV: {str(e)}")

def get_openai_client():
    """Crea y retorna el cliente de OpenAI"""
    config = load_config()
    return OpenAI(api_key=config['api_key']) 