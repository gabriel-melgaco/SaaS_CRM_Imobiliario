import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from project.settings import FROM_EMAIL



def send_email(to_email, html_content, var_html_content, subject, instance):
    message = Mail(
            from_email= FROM_EMAIL,
            to_emails= to_email,
            subject= subject,
            html_content= render_to_string(f"{html_content}.html", var_html_content)
        )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

