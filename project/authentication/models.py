from django.db import models
from django.contrib.auth.models import User
from public_app.models import Client

class TenantUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    tenant = models.ForeignKey(Client, on_delete=models.PROTECT, null=True)
    function = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.tenant.name}"