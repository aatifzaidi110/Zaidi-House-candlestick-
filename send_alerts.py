# === FILE: send_alerts.py ===

import smtplib
from email.message import EmailMessage

def send_email_alert(ticker, message):
    try:
        sender = "aatif.zaidi110@gmail.com"
        password = "your_app_password"
        recipient = "aatif.zaidi110@gmail.com"

        msg = EmailMessage()
        msg["Subject"] = f"📈 Alert for {ticker}"
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("📬 Email alert sent!")
    except Exception as e:
        print(f"❌ Email send error: {e}")

def send_sms_alert(ticker, message):
    # Optional: Use Twilio or another API
    print(f"📲 SMS alert for {ticker}: {message}")

if enable_institution_alerts and institution_value > 2_000_000:
    send_email_alert(ticker, alert_message)

