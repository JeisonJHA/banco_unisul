from django.contrib import admin

# Register your models here.
from banco_unisul.models import *

admin.site.register(ClientePF)
admin.site.register(ClientePJ)
admin.site.register(Conta)
admin.site.register(Socio)
admin.site.register(Trasnferencia)
admin.site.register(Deposito)
admin.site.register(Saque)

