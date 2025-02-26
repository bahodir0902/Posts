from django.core.mail import send_mail,EmailMessage, EmailMultiAlternatives
from .models import Code
from .utils import generate_code
from threading import Thread
def send_email_letter():
    send_mail(
        subject='TEST subject',
        message='This is a test message',
        from_email='vbahodir00@gmail.com',
        recipient_list=['vbahodir0@gmail.com']
    )

def send_file():
    file = 'CSAPP_2016.pdf'

    email = EmailMessage(
        subject='Test',
        body='test message',
        from_email='vbahodir00@gmail.com',
        to= ['vbahodir0@gmail.com']
    )

    with open(file, 'rb') as f:
        email.attach(file, f.read(), "application/pdf")

    email.send()

def send_email_alternative(receiver, user):
    code = generate_code()
    Code.objects.create(code_number=code, user_id=user.id)

    subject = 'Verify Your Email'
    text_content = f"""
    Hello {user.username},

    We received a request to verify your email address. 

    Your 4-digit passcode is: {code}

    Enter this code on the website to complete your verification.

    If you didn't request this, you can safely ignore this email.

    Best regards,  
    Your Company Team
    """

    from_email = 'vbahodir00@gmail.com'
    to = [receiver]

    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2 style="color: #333;">Hello, {user.username} 👋</h2>
        <p style="color: #555; font-size: 16px;">
            We received a request to verify your email address.
        </p>
        <p style="color: #333; font-size: 18px; font-weight: bold; text-align: center;">
            Your 4-digit passcode: <span style="color: #007BFF;">{code}</span>
        </p>
        <p style="color: #555; font-size: 16px;">
            Enter this code on the website to complete your verification.
        </p>
        <p style="color: #777; font-size: 14px;">
            If you didn’t request this, you can safely ignore this email.
        </p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
        <p style="color: #888; font-size: 12px;">
            If you need help, please contact our support team.
        </p>
        <p style="color: #888; font-size: 12px;">
            Best regards, <br>
            <strong>Your Company Team</strong>
        </p>
    </div>
    """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')

    send_thread = Thread(target=email.send)
    send_thread.start()
    # email.send()


def send_email_async():
    thread1 = Thread(target=send_email_alternative())
    thread1.start()
    # thread1.join() NO USEFUL IN THIS CONTEXT
