import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(qr_code):
# Email settings
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587
    from_email = "pierrekuh@yahoo.fr"
    to_email = "hugo.fugeray@gmail.com"
    email_password = "opoSmd9QNjvx*"

    # Create an email message object
    msg = MIMEMultipart()
    msg["Subject"] = "QR Code"
    msg["From"] = from_email
    msg["To"] = to_email

    # Add text content to the email
    text_content = "Here is the QR code you requested:"
    msg.attach(MIMEText(text_content))

    # Attach the QR code image file to the email
    msg.attach(qr_code)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use TLS for security
        server.login(from_email, email_password)
        server.send_message(msg)

    print("mail_sent with qr code :", qr_code)