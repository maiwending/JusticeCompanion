import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for credentials and settings
# Copy .env.example to .env and fill in your values, or set environment variables directly.

GMAIL_USER = os.getenv('GMAIL_USER', '')
SMARTINMATE_URL = 'https://www.smartinmate.com/my-messages.cfm'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Fill in your API key or path to local LLM

USERNAME = os.getenv('SMARTINMATE_USERNAME', '')
PASSWORD = os.getenv('SMARTINMATE_PASSWORD', '')

SMARTINMATE_USERNAME = USERNAME
SMARTINMATE_PASSWORD = PASSWORD
