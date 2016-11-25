from __future__ import unicode_literals

from django.db import models

# Create your models here.

# class User(models.Model):
#     login = models.CharField(max_length=50)
#     senha = models.CharField(max_length=50)
#     tipousuario = models.IntegerField()


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    # tpCliente = models.IntegerField()
    endereco = models.CharField(max_length=200)
    agencia = models.CharField(max_length=10)


class ClientePF(Cliente):
    CPF = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class ClientePJ(Cliente):
    CNPJ = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Conta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tpConta = models.IntegerField()
    saldo = models.IntegerField()
    chespecial = models.IntegerField()
    flespecial = models.BooleanField()

    def __str__(self):
        return self.choice_text


class Socio(models.Model):
    cliente = models.ForeignKey(ClientePF, on_delete=models.CASCADE)
    empresa = models.ForeignKey(ClientePJ, on_delete=models.CASCADE)