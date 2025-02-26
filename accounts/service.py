from django.core.mail import send_mail,EmailMessage, EmailMultiAlternatives
from .models import Code, Code_Email
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

def send_email_to_change_password(receiver, user):
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
    thread1 = Thread(target=send_email_to_change_password)
    thread1.start()
    # thread1.join() NO USEFUL IN THIS CONTEXT


def send_email_verification(receiver_email, first_name):
    code = generate_code()
    Code_Email.objects.create(code_number=code, email=receiver_email)

    subject = 'Confirm Your Email Address'
    text_content = f"""
    Hello {first_name},

    Thank you for signing up! To secure your account, please verify your email address.

    Your 4-digit verification code is: {code}

    Enter this code on our website to complete the verification process.

    If you didn’t request this, please ignore this email.

    Best regards,  
    Your Company Team
    """

    from_email = 'vbahodir00@gmail.com'
    to = [receiver_email]

    html_content = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; background: #f9f9f9; padding: 40px 20px;">
      <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #6D5DF6, #1E90FF); padding: 20px; text-align: center;">
          <h1 style="color: #fff; margin: 0; font-size: 28px;">Verify Your Email 🚀</h1>
        </div>
        <!-- Main Content -->
        <div style="padding: 30px; text-align: center;">
          <p style="color: #555; font-size: 16px; margin-bottom: 20px;">
            You're just one step away from activating your account!
          </p>
          <div style="background: #F4F8FF; border-radius: 8px; padding: 15px 20px; display: inline-block; margin-bottom: 20px;">
            <span style="color: #1E90FF; font-size: 20px; font-weight: bold;">Your Verification Code:</span>
            <div style="color: #6D5DF6; font-size: 36px; font-weight: bold; margin-top: 10px;">
              {code}
            </div>
          </div>
          <p style="color: #555; font-size: 16px; margin-bottom: 30px;">
            Enter this code on our website to complete the verification process.
          </p>
        </div>
        <!-- Footer -->
        <div style="background: #f1f1f1; padding: 15px 20px; text-align: center;">
          <p style="color: #888; font-size: 12px; margin: 0;">
            If you didn’t request this email, please ignore it.
          </p>
          <p style="color: #888; font-size: 12px; margin: 5px 0 0;">
            Need help? <a href="mailto:support@yourcompany.com" style="color: #1E90FF; text-decoration: none;">Contact our support team</a>.
          </p>
          <p style="color: #888; font-size: 12px; margin: 15px 0 0;">
            Best regards,<br>
            <strong>Your Company Team</strong>
          </p>
        </div>
      </div>
    </div>
    """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')

    send_thread = Thread(target=email.send)
    send_thread.start()