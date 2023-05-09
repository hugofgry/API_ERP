import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO

def send_email(qr_code,receiver_email):


    img_buf = BytesIO()
    img = qr_code.make_image(fill_color="black", back_color="white")
    img.save(img_buf, format='PNG')
    img_data = img_buf.getvalue()

    gmail_user = "payetonkawadeveloppeurs@gmail.com"
    gmail_password = "jvgxdzpyebfsjhde"

    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = receiver_email
        msg['Subject'] = 'Your QR Code'

        body = 'Please find the attached QR code.'
        msg.attach(MIMEText(body, 'plain'))

        image = MIMEImage(img_data, name="qrcode.png", _subtype='png')
        msg.attach(image)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, receiver_email, msg.as_string())
        server.quit()
        print('Email sent!')
    except Exception as e:
        print(f'Error occurred: {e}')