import ssl
import smtplib
import os
from decouple import config

port = 465  # For SSL
receiver_email = 'dahlia.dry24@gmail.com'
sender_email = 'teg.dashboard@gmail.com'
message= """Subject: testing

hello :) """

def send(receiver_emails, message):
    """This function sends an automated email from the account teg.dashboard@gmail.com
    receiver_emails: list of recipieints
    message: email content. First line should contain Subject: [subject]."""
    # Create a secure SSL context
    context = ssl.create_default_context()       
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, config('EMAIL_PASSWORD'))
            for recipient in receiver_emails:
                server.sendmail(sender_email, recipient, message)
            server.quit()
        return 'success'
    except Exception as e:
        return f'email send failed with message {e}'