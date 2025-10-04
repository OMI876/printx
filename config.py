import os
from dotenv import load_dotenv

load_dotenv()  # .env file load karega

EMAIL_ADDRESS = "apikey"   # SendGrid ka username fix hota hai
EMAIL_PASSWORD = os.getenv("SENDGRID_API_KEY")  # Ab env se le raha hai
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # optional: env me bhi daal sakta hai
