# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('endereco', models.CharField(max_length=200)),
                ('agencia', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tpconta', models.IntegerField()),
                ('saldo', models.IntegerField()),
                ('chespecial', models.IntegerField()),
                ('flespecial', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('dtdeposito', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Saque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('dtsaque', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Trasnferencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('dttransferencia', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ClientePF',
            fields=[
                ('cliente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='banco_unisul.Cliente')),
                ('CPF', models.CharField(max_length=30)),
            ],
            bases=('banco_unisul.cliente',),
        ),
        migrations.CreateModel(
            name='ClientePJ',
            fields=[
                ('cliente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='banco_unisul.Cliente')),
                ('CNPJ', models.CharField(max_length=30)),
            ],
            bases=('banco_unisul.cliente',),
        ),
        migrations.AddField(
            model_name='trasnferencia',
            name='destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinotransferencia', to='banco_unisul.Cliente'),
        ),
        migrations.AddField(
            model_name='trasnferencia',
            name='origem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origemtransferencia', to='banco_unisul.Cliente'),
        ),
        migrations.AddField(
            model_name='saque',
            name='origem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco_unisul.Cliente'),
        ),
        migrations.AddField(
            model_name='deposito',
            name='destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco_unisul.Cliente'),
        ),
        migrations.AddField(
            model_name='conta',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco_unisul.Cliente'),
        ),
        migrations.AddField(
            model_name='socio',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco_unisul.ClientePF'),
        ),
        migrations.AddField(
            model_name='socio',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco_unisul.ClientePJ'),
        ),
    ]
