from app.core.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_otp(email: str, otp: str) -> None:
    # Thông tin email của bạn
    sender_email = settings.EMAIL_USER  # Thay bằng email của bạn
    sender_password = settings.EMAIL_PASSWORD  # Thay bằng mật khẩu ứng dụng

    # Cấu hình SMTP Server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Tạo nội dung email
    subject = "Your OTP Code"
    body = f"Hello,\n\nYour OTP code is: {otp}\n\nThank you!"

    # Email MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Kết nối tới SMTP Server và gửi email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Kích hoạt bảo mật TLS
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, email, message.as_string())
    server.quit()

    print(f"Email sent to {email}")
