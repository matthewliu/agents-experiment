import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
DATABASE_URL = os.getenv('DATABASE_URL')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
