from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import TemplateView
from banco_unisul.forms import UserForm
from .models import *

login_template = 'banco_unisul/login.html'


def go_web(request, user):
    if user.groups.filter(name='gerente').exists():
        return render(request, 'banco_unisul/bancointero.html')
    elif user.groups.filter(name='cliente').exists():
        conta = Conta.objects.all().select_related("cliente").filter(cliente__nome__exact=user).get()
        return render(request, 'banco_unisul/bancoexterno.html', {'conta': conta})
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


class BasicView(LoginRequiredMixin, TemplateView):
    raise_exception = True

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


class ContaCreate(LoginRequiredMixin, CreateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']
    success_url = reverse_lazy('banco_unisul:index')

    def get_initial(self):
        try:
            pk = self.kwargs['pk']
            return {
                'cliente': pk,
            }
        except:
            return {}


class ContaUpdate(LoginRequiredMixin, UpdateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']


class ContaDelete(LoginRequiredMixin, DeleteView):
    model = Conta
    success_url = reverse_lazy('banco_unisul:index')


class ClientePFCreate(LoginRequiredMixin, CreateView):
    model = ClientePF
    fields = ['nome', 'endereco', 'agencia', 'CPF']


class ClientePFUpdate(LoginRequiredMixin, UpdateView):
    model = ClientePF
    fields = ['nome', 'endereco', 'agencia', 'CPF']


class ClientePFDelete(LoginRequiredMixin, DeleteView):
    model = ClientePF
    success_url = reverse_lazy('banco_unisul:index')


class ClientePJCreate(LoginRequiredMixin, CreateView):
    model = ClientePJ
    fields = ['nome', 'endereco', 'agencia', 'CNPJ']


class ClientePJUpdate(LoginRequiredMixin, UpdateView):
    model = ClientePJ
    fields = ['nome', 'endereco', 'agencia', 'CNPJ']


class ClientePJDelete(LoginRequiredMixin, DeleteView):
    model = ClientePJ
    success_url = reverse_lazy('banco_unisul:index')


class Cad_ClienteView(BasicView):
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


class SocioView(LoginRequiredMixin, CreateView):
    model = Socio
    fields = ['cliente', 'empresa']


class SocioUpdate(LoginRequiredMixin, UpdateView):
    model = Socio
    fields = ['cliente', 'empresa']


class SocioDelete(LoginRequiredMixin, DeleteView):
    model = Socio
    success_url = reverse_lazy('banco_unisul:index')


class SaqueView(LoginRequiredMixin, CreateView):
    model = Saque
    fields = ['origem', 'valor']
    context_object_name = 'conta'

    def get_context_data(self, **kwargs):
        print('get_context_data')
        context = super(SaqueView, self).get_context_data(**kwargs)
        context['conta'] = Conta.objects.all().select_related("cliente").filter(cliente__nome__exact=self.request.user).get()
        return context

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'origem': pk,
        }


class DepositoView(LoginRequiredMixin, CreateView):
    model = Deposito
    fields = ['destino', 'valor']

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'destino': pk,
        }


class TransferenciaView(LoginRequiredMixin, CreateView):
    model = Trasnferencia
    fields = ['origem', 'destino', 'valor']
    context_object_name = 'conta'

    def get_context_data(self, **kwargs):
        context = super(TransferenciaView, self).get_context_data(**kwargs)
        context['conta'] = Conta.objects.all().select_related("cliente").filter(cliente__nome__exact=self.request.user).get()
        context['destino'] = Conta.objects.all().select_related("cliente").exclude(cliente__nome__exact=self.request.user).all()
        return context

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'origem': pk,
        }


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


class TodosClientesView(LoginRequiredMixin, generic.ListView):
    template_name = 'banco_unisul/todoscliente.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return Cliente.objects.all()


class TodosClientesPJView(LoginRequiredMixin, generic.ListView):
    template_name = 'banco_unisul/todosclientepj.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return ClientePJ.objects.all()


class DetalhepfView(LoginRequiredMixin, generic.DetailView):
    model = Cliente
    template_name = 'banco_unisul/detalhepf.html'

    def get_context_data(self, **kwargs):
        context = super(DetalhepfView, self).get_context_data(**kwargs)
        context['CPF'] = ClientePF.objects.all().filter(id=self.kwargs['pk']).get().CPF
        return context


class DetalhepjView(LoginRequiredMixin, generic.DetailView):
    model = Cliente
    template_name = 'banco_unisul/detalhepj.html'

    def get_context_data(self, **kwargs):
        context = super(DetalhepjView, self).get_context_data(**kwargs)
        context['CNPJ'] = ClientePJ.objects.all().filter(id=self.kwargs['pk']).get().CNPJ
        context['socios'] = Socio.objects.all().filter(empresa=self.kwargs['pk'])
        return context


class DetalheContaView(LoginRequiredMixin, generic.DetailView):
    model = Conta
    template_name = 'banco_unisul/detalheconta.html'


class Conta_ClienteView(LoginRequiredMixin, CreateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'cliente': pk,
        }


class EmpresaSocioView(LoginRequiredMixin, CreateView):
    model = Socio
    fields = ['empresa', 'cliente']

    def get_initial(self):
        pk = self.kwargs['pk']
        return {
            'empresa': pk,
        }


class ListaContaView(LoginRequiredMixin, generic.ListView):
    model = Conta
    template_name = 'banco_unisul/listaconta.html'
    context_object_name = 'todos_contas'

    def get_queryset(self):
        return Conta.objects.all()


class SocioExclusao(LoginRequiredMixin, generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluisocio.html'
    context_object_name = 'todos_socios'

    def get_queryset(self):
        return Socio.objects.all().select_related("cliente")


class ContaExclusao(LoginRequiredMixin, generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluiconta.html'
    context_object_name = 'todas_contas'

    def get_queryset(self):
        return Conta.objects.all().select_related("cliente")


class ListaPFExclusao(LoginRequiredMixin, generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluiuclientepf.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return ClientePF.objects.all()


class ListaPJExclusao(LoginRequiredMixin, generic.ListView):
    model = Socio
    template_name = 'banco_unisul/listaexcluiclientepj.html'
    context_object_name = 'todos_clientes'

    def get_queryset(self):
        return ClientePJ.objects.all()


class DadosRelatorioView(LoginRequiredMixin, generic.ListView):
    model = Cliente
    template_name = 'banco_unisul/dadosrelatorio.html'
    context_object_name = 'dados_relatorio'

    def get_queryset(self):
        return ClientePJ.objects.all()


class SaqueListView(LoginRequiredMixin, generic.ListView):
    model = Saque
    template_name = 'banco_unisul/saquelista.html'
    context_object_name = 'conta'

    def get_queryset(self):
        return Conta.objects.all().select_related("cliente").filter(cliente__nome__exact=self.request.user).get()


class DepositoListView(LoginRequiredMixin, generic.ListView):
    model = Deposito
    template_name = 'banco_unisul/depositolista.html'
    context_object_name = 'conta'

    def get_queryset(self):
        return Conta.objects.all().select_related("cliente").filter(cliente__nome__exact=self.request.user).get()


class TransferenciaListView(LoginRequiredMixin, generic.ListView):
    model = Trasnferencia
    template_name = 'banco_unisul/transferencialista.html'
    context_object_name = 'conta'

    def get_queryset(self):
        return Conta.objects.all().select_related("cliente").filter(cliente__nome__exact=self.request.user).get()