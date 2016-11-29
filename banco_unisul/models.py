# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import render, redirect
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

    def limite(self):
        if self.flespecial:
            return self.saldo + self.chespecial
        else:
            return self.saldo



class Socio(models.Model):
    cliente = models.ForeignKey(ClientePF, on_delete=models.CASCADE)
    empresa = models.ForeignKey(ClientePJ, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('cliente', 'empresa'),)

    def __str__(self):
        return 'Socio: ' + self.cliente.nome + ' - Empresa: ' + self.empresa.nome

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('banco_unisul:detalhepj', kwargs={'pk': self.empresa.id})


class Trasnferencia(models.Model):
    origem = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='origemtransferencia')
    destino = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='destinotransferencia')
    valor = models.IntegerField()
    dttransferencia = models.DateTimeField("Data da transferencia", auto_now_add=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('banco_unisul:index')

    def clean(self):
        corigem = Conta.objects.get(cliente=self.origem.cliente)
        if corigem.limite() < self.valor:
            raise ValidationError(corigem.cliente.nome + " não possui saldo suficiente.")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        corigem = Conta.objects.get(cliente=self.origem.cliente)
        cdestino = Conta.objects.get(cliente=self.destino.cliente)
        if corigem.limite() >= self.valor:
            cdestino.saldo += self.valor
            corigem.saldo -= self.valor
            corigem.save()
            cdestino.save()
        else:
            raise Exception(corigem.cliente.nome + " não possui saldo suficiente.")

        super(Trasnferencia, self).save(force_insert, force_update, using, update_fields)

class Saque(models.Model):
    origem = models.ForeignKey(Conta, on_delete=models.CASCADE)
    valor = models.IntegerField()
    dtsaque = models.DateTimeField("Data do saque", auto_now_add=True)
    template = 'banco_unisul:index'

    def get_absolute_url(self):
        print('get_absolute_url')
        from django.urls import reverse
        return reverse(self.template)

    def clean(self):
        corigem = Conta.objects.get(cliente=self.origem.cliente)
        if corigem.limite() < self.valor:
            raise ValidationError(corigem.cliente.nome + " não possui saldo suficiente.")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        corigem = Conta.objects.get(cliente=self.origem.cliente)
        corigem.saldo -= self.valor
        corigem.save()

        super(Saque, self).save(force_insert, force_update, using, update_fields)


class Deposito(models.Model):
    destino = models.ForeignKey(Conta, on_delete=models.CASCADE)
    valor = models.IntegerField()
    dtdeposito = models.DateTimeField("Data do deposito", auto_now_add=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('banco_unisul:index')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        cdestino = Conta.objects.get(cliente=self.destino.cliente)
        cdestino.saldo += self.valor
        cdestino.save()
        super(Deposito, self).save(force_insert, force_update, using, update_fields)