from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User
import random
from django.utils.timezone import localtime
from project.settings import DOMAIN_NAME
import pytz

fuso_horario = pytz.timezone('America/Sao_Paulo')

def domain_correction(domain): #delete when deploy at production environment    
    new_domain = str()

    for i in domain:
        if i in [':', '5', '0', '8']:
            pass
        else:
            new_domain+=i
    return new_domain

class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.code = random.randint(1000, 9999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
    
class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
        

class Client(TenantMixin):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    company_name = models.CharField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    paid_until = models.DateField(blank=True, null=True)
    on_trial = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)
    dns_name = models.CharField(max_length=20, unique=True)
    telephone = models.CharField(max_length=20)
    activation = models.BooleanField(default=True)

    auto_create_schema = True #Creating a schema at DB


    def save(self, *args, **kwargs):
        # Salva o Tenant (cria o schema)
        super().save(*args, **kwargs)

        if not Domain.objects.filter(tenant=self).exists(): #check if the domain already exists
            domain = f"{self.dns_name.lower().replace(' ', '')}.{domain_correction(DOMAIN_NAME)}"  # create a new domain
            Domain.objects.create(domain=domain, tenant=self, is_primary=True)


    def __str__(self):
        return self.company_name

class Domain(DomainMixin):
    pass


class ClientInventory(models.Model):
    client_count = models.IntegerField()
    client_plan = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] #ordering by created_at decreasing

    def __str__(self):
        return f'{self.client_count} - {self.client_plan}'

