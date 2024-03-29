import os
from dotenv import load_dotenv

load_dotenv()

# Required
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MONGODB_URI = os.getenv('MONGODB_URI')

# Optional
FRONTEND_URL = os.getenv('FRONTEND_URL')
