from django.db.models.signals import post_save
from django.dispatch import receiver
from public_app.models import Client, ActivationCode, ResetPassword, ClientInventory
from django.contrib.auth.models import User
from public_app.sendgrid import send_email
from project.settings import DOMAIN_NAME


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        activation_code = ActivationCode(user=instance)
        activation_code.save()
       
        send_email(to_email=instance.email, 
                   html_content='activation_email', 
                   var_html_content={
                        'activation_code': activation_code.code,
                        'user_id': instance.id,
                        'domain_name': DOMAIN_NAME,
                    }, 
                   subject='IMOVASE- Ativação de conta', 
                   instance=instance,
            )
        
        
@receiver(post_save, sender=ResetPassword)
def send_password_reset_email(sender, instance, created, **kwargs):
    if created:

        send_email(to_email=instance.user.email,
                   html_content='reset_email',
                   var_html_content={
                        'token': instance.token,
                        'domain_name': DOMAIN_NAME,
                   },
                    subject='IMOVASE- Redefinição de senha',
                    instance=instance,

        )


@receiver(post_save, sender=Client)
def register_client_post_save(sender, instance, **kwargs):
    client_count = Client.objects.count()
    ClientInventory.objects.create(client_count=client_count)