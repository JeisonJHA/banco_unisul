from django import forms
from django.contrib.auth.models import User

from .models import ClientePF, ClientePJ, Conta, Socio


class ClientePFForm(forms.ModelForm):

    class Meta:
        model = ClientePF
        fields = ['nome', 'endereco', 'dtnascimento', 'CPF']


class ClientePJForm(forms.ModelForm):

    class Meta:
        model = ClientePJ
        fields = ['nome', 'endereco', 'CNPJ']


class ContaForm(forms.ModelForm):

    class Meta:
        model = Conta
        fields = ['cliente', 'agencia', 'saldo', 'tpconta', 'flespecial', 'chespecial']


class SocioForm(forms.ModelForm):

    class Meta:
        model = Socio
        fields = ['cliente', 'empresa']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']