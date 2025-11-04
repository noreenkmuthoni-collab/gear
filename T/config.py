import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
SENDER_EMAIL = "maxxichorea@gmail.com"
SENDER_NAME = "Cold Email Automation"

# API Keys (set these in .env file)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")

# Gmail API Credentials
GMAIL_CREDENTIALS_FILE = "credentials.json"
GMAIL_TOKEN_FILE = "token.json"
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Application Settings
APP_PORT = 5000
DEBUG = True

# Theme Colors
THEME_COLORS = {
    "primary": "#FF1493",  # Pink
    "secondary": "#000000",  # Black
    "accent": "#FF69B4",  # Hot Pink
    "background": "#1a1a1a",  # Dark background
    "text": "#ffffff"
}
