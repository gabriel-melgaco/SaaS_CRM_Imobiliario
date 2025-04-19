from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from public_app.models import Client
from property.models import Property

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('company_name', 'telephone', 'created_on', 'on_trial', 'activation')


@admin.register(Property)
class PropertyAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'code', 'zip_code', 'neighborhood', 'state', 'street')