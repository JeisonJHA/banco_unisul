from django.contrib import admin

# Register your models here.
from banco_unisul.models import ClientePF, ClientePJ, Conta, Socio

admin.site.register(ClientePF)
admin.site.register(ClientePJ)
admin.site.register(Conta)
admin.site.register(Socio)
