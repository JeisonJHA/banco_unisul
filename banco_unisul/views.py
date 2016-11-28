# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import Group, User

from banco_unisul.forms import UserForm
from .models import *

login_template = 'banco_unisul/login.html'


def go_web(request, user):
    if user.groups.filter(name='gerente').exists():
        return render(request, 'banco_unisul/bancointero.html')
    elif user.groups.filter(name='cliente').exists():
        return render(request, 'banco_unisul/bancoexterno.html')
    else:
        return render(request, login_template)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return go_web(request, user)
            else:
                return render(request, login_template, {'error_message': 'Your account has been disabled'})
        else:
            return render(request, login_template, {'error_message': 'Invalid login'})
    return render(request, login_template)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, login_template, context)


class BasicView(PermissionRequiredMixin, generic.View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, login_template)
        else:
            return render(request, self.template_name, self.context)


class IndexView(generic.View):
    template_name = 'banco_unisul/index.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, login_template)
        else:
            return go_web(request, request.user)


class ContaCreate(CreateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']
    success_url = reverse_lazy('banco_unisul:index')


class ContaUpdate(UpdateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']


class ContaDelete(DeleteView):
    model = Conta
    success_url = reverse_lazy('banco_unisul:index')


class ClientePFCreate(CreateView):
    model = ClientePF
    fields = ['nome', 'endereco', 'agencia', 'CPF']


class ClientePFUpdate(UpdateView):
    model = ClientePF
    fields = ['nome', 'endereco', 'agencia', 'CPF']


class ClientePFDelete(DeleteView):
    model = ClientePF
    success_url = reverse_lazy('banco_unisul:index')


class ClientePJCreate(CreateView):
    model = ClientePJ
    fields = ['nome', 'endereco', 'agencia', 'CNPJ']


class ClientePJUpdate(UpdateView):
    model = ClientePJ
    fields = ['nome', 'endereco', 'agencia', 'CNPJ']


class ClientePJDelete(DeleteView):
    model = ClientePJ
    success_url = reverse_lazy('banco_unisul:index')


class Cad_ClienteView(BasicView):
    permission_required = 'cliente'
    template_name = 'banco_unisul/cad_cliente.html'
    context = {

    }


class Cad_ContaView(BasicView):
    permission_required = 'cliente'
    template_name = 'banco_unisul/cad_conta.html'
    context = {

    }


class Cad_SocioView(BasicView):
    template_name = 'banco_unisul/cad_socio.html'
    context = {

    }


class RelatorioView(BasicView):
    template_name = 'banco_unisul/relatorio.html'
    context = {

    }


class SocioView(CreateView):
    model = Socio
    fields = ['cliente', 'empresa']


class SocioUpdate(UpdateView):
    model = Socio
    fields = ['cliente', 'empresa']


class SocioDelete(DeleteView):
    model = Socio
    success_url = reverse_lazy('banco_unisul:index')


class SaqueView(CreateView):
    model = Saque
    fields = ['origem', 'valor', 'dtsaque']


class DepositoView(CreateView):
    model = Deposito
    fields = ['destino', 'valor', 'dtdeposito']


class TransferenciaView(CreateView):
    model = Trasnferencia
    fields = ['origem', 'destino', 'valor', 'dttransferencia']


class AlteraClientePF(BasicView):
    template_name = 'banco_unisul/alteraclientepf.html'
    clientes = ClientePF.objects.all()
    context = {
        'clientes': clientes
    }


class AlteraClientePJ(BasicView):
    template_name = 'banco_unisul/alteraclientepj.html'
    clientes = ClientePJ.objects.all()
    context = {
        'clientes': clientes
    }


class Alt_ContaView(BasicView):
    template_name = 'banco_unisul/alteraconta.html'
    contas = Conta.objects.all()
    context = {
        'contas': contas
    }


class TodosClientesView(generic.ListView):
    template_name = 'banco_unisul/todoscliente.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return Cliente.objects.all()


class TodosClientesPJView(generic.ListView):
    template_name = 'banco_unisul/todosclientepj.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return ClientePJ.objects.all()


class DetalhepfView(generic.DetailView):
    model = Cliente
    template_name = 'banco_unisul/detalhepf.html'

    def get_context_data(self, **kwargs):
        context = super(DetalhepfView, self).get_context_data(**kwargs)
        context['CPF'] = ClientePF.objects.all().filter(id=self.kwargs['pk']).get().CPF
        return context


class DetalhepjView(generic.DetailView):
    model = Cliente
    template_name = 'banco_unisul/detalhepj.html'

    def get_context_data(self, **kwargs):
        context = super(DetalhepjView, self).get_context_data(**kwargs)
        context['CNPJ'] = ClientePJ.objects.all().filter(id=self.kwargs['pk']).get().CNPJ
        context['socios'] = Socio.objects.all().filter(empresa=self.kwargs['pk'])
        return context


class DetalheContaView(generic.DetailView):
    model = Conta
    template_name = 'banco_unisul/detalheconta.html'


class Conta_ClienteView(CreateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'cliente': pk,
        }


class EmpresaSocioView(CreateView):
    model = Socio
    fields = ['empresa', 'cliente']

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'empresa': pk,
        }


class ListaContaView(generic.ListView):
    model = Conta
    template_name = 'banco_unisul/listaconta.html'
    context_object_name = 'todos_contas'

    def get_queryset(self):
        return Conta.objects.all()


class SocioExclusao(generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluisocio.html'
    context_object_name = 'todos_socios'

    def get_queryset(self):
        return Socio.objects.all().select_related("cliente")


class ContaExclusao(generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluiconta.html'
    context_object_name = 'todas_contas'

    def get_queryset(self):
        return Conta.objects.all().select_related("cliente")


class ListaPFExclusao(generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluiuclientepf.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return ClientePF.objects.all()


class ListaPJExclusao(generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluiclientepj.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return ClientePJ.objects.all()