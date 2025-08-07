import smtplib
from email.message import EmailMessage

def send_strategy_email(recipient, signal_data):
    """
    Sends an email alert with strategy recommendation based on big money activity.
    
    Parameters:
    - recipient (str): recipient email address
    - signal_data (dict): dictionary returned by generate_strategy()
    """

    subject = f"🚨 Strategy Alert: {signal_data['ticker']} — {signal_data['strategy']}"
    content = f"""
📊 Strategy Alert

Ticker: {signal_data['ticker']}
Current Price: ${signal_data['price']:.2f}
Signal Type: {signal_data['signal_type']}

🧠 Strategy Recommendation: {signal_data['strategy']}
📌 Reason: {signal_data['explanation']}
🔜 Next Step: {signal_data['next_step']}

Powered by Big Money Tracker
    """

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = "your_email@gmail.com"
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("your_email@gmail.com", "your_app_password")  # Use app-specific password
            smtp.send_message(msg)
            print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
