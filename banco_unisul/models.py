from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.urls import reverse

from django.db import models

# Create your models here.


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    agencia = models.CharField(max_length=10)

    def __str__(self):
        return self.nome

    def is_PJ(self):
        try:
            p = ClientePJ.objects.all().filter(id=self.id).get().CNPJ
            return True
        except:
            return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            from django.contrib.auth.models import User
            user = User.objects.create_user(self.nome, password='pass1234')
            user.groups.add(Group.objects.get(name='cliente'))
            user.save()
        super(Cliente, self).save(force_insert, force_update, using, update_fields)

    class META:
        abstract = True


class ClientePF(Cliente):
    CPF = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('banco_unisul:detalhepf', kwargs={'pk': self.pk})


class ClientePJ(Cliente):
    CNPJ = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('banco_unisul:detalhepj', kwargs={'pk': self.pk})


class Conta(models.Model):
    TIPO_CONTA = (
        (1, 'ContaCorrente'),
        (2, 'ContaPoupanca'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tpconta = models.IntegerField("Tipo da Conta", choices=TIPO_CONTA)
    saldo = models.IntegerField()
    chespecial = models.IntegerField("Limite cheque especial")
    flespecial = models.BooleanField("Utiliza cheque especial")

    class META:
        unique_together = (("cliente", "tpconta"),)

    def __str__(self):
        try:
            return self.get_tpconta_display() + ' - ' + self.cliente.nome + ' - ' + ClientePF.objects.get(id=self.cliente.id).CPF
        except:
            return self.get_tpconta_display() + ' - ' + self.cliente.nome + ' - ' + ClientePJ.objects.get(id=self.cliente.id).CNPJ

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('banco_unisul:detalheconta', kwargs={'pk': self.pk})

    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     queryset = Conta.objects.filter(cliente=self.cliente, tpconta=self.tpconta)
    #     if queryset.exists():
    #         print 'ERROR!'
    #         raise ValidationError("This row already exists")


class Socio(models.Model):
    cliente = models.ForeignKey(ClientePF, on_delete=models.CASCADE)
    empresa = models.ForeignKey(ClientePJ, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('cliente', 'empresa'),)

    def __str__(self):
        return 'Socio: ' + self.cliente.nome + ' - Empresa: ' + self.empresa.nome

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('banco_unisul:detalhepf', kwargs={'pk': self.empresa.id})


class Trasnferencia(models.Model):
    origem = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='origemtransferencia')
    destino = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='destinotransferencia')
    valor = models.IntegerField()
    dttransferencia = models.DateTimeField("Data da transferencia")


class Saque(models.Model):
    origem = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor = models.IntegerField()
    dtsaque = models.DateTimeField("Data do saque")


class Deposito(models.Model):
    destino = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor = models.IntegerField()
    dtdeposito = models.DateTimeField("Data do deposito")