import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from django.core.mail import send_mail


def send_email_notification(to_email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)



# def send_email_notification(to_email, subject, message):
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     sender_email = settings.EMAIL_HOST_USER
#     sender_password = settings.EMAIL_HOST_PASSWORD

#     msg = MIMEText(message)
#     msg['Subject'] = subject
#     msg['From'] = sender_email
#     msg['To'] = to_email

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, [to_email], msg.as_string())
#         server.quit()
#         print(f"تم إرسال البريد إلى {to_email}")
#     except Exception as e:
#         print(f"فشل إرسال البريد إلى {to_email}: {e}")
