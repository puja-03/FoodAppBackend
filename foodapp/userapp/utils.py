import os
import random
from django.core.mail import send_mail, EmailMessage
from .models import *
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]

        )
        email.send()

def send_otp_email(email):
    subject = 'OTP for email verification'
    otp = 1234
    message = f'Your OTP for email verification is {otp}'
    html_message = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #ff6f61;
                padding: 20px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
                margin: 0;
            }}
            .content {{
                padding: 30px;
                text-align: center;
            }}
            .content h1 {{
                font-size: 24px;
                color: #333333;
                margin-bottom: 20px;
            }}
            .content p {{
                font-size: 16px;
                color: #555555;
                line-height: 1.6;
            }}
            .otp-box {{
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 8px;
                display: inline-block;
                margin: 20px 0;
            }}
            .otp {{
                font-size: 32px;
                font-weight: bold;
                color: #ff6f61;
                letter-spacing: 5px;
            }}
            .footer {{
                background-color: #f9f9f9;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                color: #777777;
            }}
            .footer a {{
                color: #ff6f61;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header Section -->
            <div class="header">
                <h1>FoodApp</h1>
            </div>
            <!-- Content Section -->
            <div class="content">
                <h1>Verify Your Email Address</h1>
                <p>Hi there,</p>
                <p>Welcome to <strong>FoodApp</strong>! We're excited to have you on board. To complete your registration, please use the OTP below to verify your email address:</p>
                
                <!-- OTP Box -->
                <div class="otp-box">
                    <div class="otp">{otp}</div>
                </div>

                <p>This OTP is valid for <strong>10 minutes</strong>. If you didn't request this, please ignore this email.</p>
                <p>Happy eating and have fun!! 🍕🍔</p>
            </div>

            <!-- Footer Section -->
            <div class="footer">
                <p>If you have any questions, feel free to <a href="mailto:support@foodapp.com">contact us</a>.</p>
                <p>&copy; 2023 FoodApp. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    from_email = os.environ.get('EMAIL_FROM')
    send_mail(subject, message, from_email, [email], html_message=html_message)
    try:
        user = CustomUser.objects.get(email=email)
        user.otp = otp
        user.otp_created_at = now()
        user.save()
    except ObjectDoesNotExist:
        return {"error": "User with this email does not exist."}
    return otp