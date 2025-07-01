import smtplib
from email.message import EmailMessage
from .config import EMAIL_FROM, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS

def send_verification_email(to_email, link):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(f"Click to verify: {link}")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)