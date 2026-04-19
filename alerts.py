import smtplib
from email.mime.text import MIMEText
import os

def send_alert(subject, message, to_email):
    from_email = os.getenv('EMAIL_USER', 'your_email@example.com')
    password = os.getenv('EMAIL_PASS', 'your_password')

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Alert sent")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# For SMS, would need Twilio
# from twilio.rest import Client
# def send_sms(message, to_number):
#     account_sid = os.getenv('TWILIO_SID')
#     auth_token = os.getenv('TWILIO_TOKEN')
#     client = Client(account_sid, auth_token)
#     client.messages.create(body=message, from_='your_twilio_number', to=to_number)