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
    from_email = os.environ.get('EMAIL_FROM')
    send_mail(subject, message, from_email, [email])
    try:
        user = CustomUser.objects.get(email=email)
        user.otp = otp
        user.otp_created_at = now()
        user.save()
    except ObjectDoesNotExist:
        return {"error": "User with this email does not exist."}
    return otp