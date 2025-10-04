import os
from dotenv import load_dotenv

# 🔸 Load environment variables from .env file
load_dotenv()

# 📨 SendGrid SMTP Configuration
# SendGrid SMTP username is always literally "apikey" (don't change this)
EMAIL_ADDRESS = "apikey"
EMAIL_PASSWORD = os.getenv("SENDGRID_API_KEY")  # Securely loaded from .env
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587

# 🧠 Sender email (the one you've verified in SendGrid)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# 🧱 MySQL Database Configuration (Railway)
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))  # Railway custom port or default 3306
