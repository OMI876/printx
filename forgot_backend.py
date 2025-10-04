from flask import Blueprint, render_template, request, jsonify
import MySQLdb.cursors, random, smtplib
from email.mime.text import MIMEText
from extensions import mysql, bcrypt
import os

# 🔸 Load SMTP / SendGrid credentials from environment (.env or Render)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "apikey")  # SendGrid username is always 'apikey'
EMAIL_PASSWORD = os.getenv("SENDGRID_API_KEY")       # Your SendGrid API Key
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.sendgrid.net")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

forgot_bp = Blueprint('forgot_bp', __name__)

# ✅ Forgot Password Page (GET)
@forgot_bp.route('/forgot', methods=['GET'])
def forgot():
    return render_template('reset_password.html')  # Your frontend reset page

# ✅ Function to send OTP via SMTP (SendGrid)
def send_otp(email, otp):
    subject = "Password Reset OTP"
    body = f"Your OTP is: {otp}"

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        print("🚀 Connecting to SMTP...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:  # ⏱ timeout fix
            print("🔐 Starting TLS...")
            server.starttls()
            print("🧠 Logging in to SendGrid...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print(f"✉️ Sending OTP to {email} ...")
            server.sendmail(SENDER_EMAIL, [email], msg.as_string())
        print("✅ OTP Email sent successfully!")
    except Exception as e:
        print(f"❌ SMTP error while sending OTP: {str(e)}")
        raise  # Let the upper route catch it and return proper error

# ✅ Step 1: Send OTP
@forgot_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"success": False, "message": "❌ Email is required"})

        # Check if user exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        account = cursor.fetchone()

        if not account:
            return jsonify({"success": False, "message": "❌ Email not found!"})

        # Generate & store OTP
        otp = str(random.randint(100000, 999999))
        cursor.execute("INSERT INTO password_resets (email, otp) VALUES (%s,%s)", (email, otp))
        mysql.connection.commit()

        # Send OTP Email
        send_otp(email, otp)

        return jsonify({"success": True, "message": "✅ OTP sent to your email."})

    except Exception as e:
        return jsonify({"success": False, "message": f"❌ Failed to send email: {str(e)}"})

# ✅ Step 2: Verify OTP
@forgot_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM password_resets 
        WHERE email=%s AND otp=%s 
        ORDER BY created_at DESC LIMIT 1
    """, (email, otp))
    record = cursor.fetchone()

    if record:
        return jsonify({"success": True, "message": "✅ OTP verified"})
    else:
        return jsonify({"success": False, "message": "❌ Invalid OTP"})

# ✅ Step 3: Reset Password
@forgot_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({"success": False, "message": "❌ Missing data"})

    hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_pw, email))
    mysql.connection.commit()

    return jsonify({"success": True, "message": "✅ Password reset successful"})
