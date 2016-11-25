# from django.template import loader
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View

from banco_unisul.forms import UserForm
from .models import *

# def index(request):
#     template = loader.get_template('index.html')
#     context = {
#
#     }
#     return HttpResponse(template.render(context, request))

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                return render(request, 'banco_unisul/banco.html')
            else:
                return render(request, 'banco_unisul/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'banco_unisul/login.html', {'error_message': 'Invalid login'})
    return render(request, 'banco_unisul/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'banco_unisul/login.html', context)

class IndexView(generic.View):
    template_name = 'banco_unisul/index.html'

    def get(self, request):
        if not self.request.user.is_authenticated():
            print 'login'
            return render(self.request, 'banco_unisul/login.html')
        else:
            return render(self.request, 'banco_unisul/banco.html')

# def index(request):
#     if not request.user.is_authenticated():
#         return render(request, 'banco_unisul/login.html')
#     else:
#         albums = Album.objects.filter(user=request.user)
#         song_results = Song.objects.all()
#         query = request.GET.get("q")
#         if query:
#             albums = albums.filter(
#                 Q(album_title__icontains=query) |
#                 Q(artist__icontains=query)
#             ).distinct()
#             song_results = song_results.filter(
#                 Q(song_title__icontains=query)
#             ).distinct()
#             return render(request, 'music/index.html', {
#                 'albums': albums,
#                 'songs': song_results,
#             })
#         else:
#             return render(request, 'music/index.html', {'albums': albums})


class ContaCreate(CreateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']


class ContaUpdate(UpdateView):
    model = Conta
    fields = ['cliente', 'tpconta', 'saldo', 'flespecial', 'chespecial']


class ContaDelete(DeleteView):
    model = Conta
    success_url = reverse_lazy('banco:index')


class ClientePFCreate(CreateView):
    model = ClientePF
    fields = ['nome', 'endereco', 'agencia', 'CPF']


class ClientePFUpdate(UpdateView):
    model = ClientePF
    fields = ['nome', 'endereco', 'agencia', 'CPF']


class ClientePFDelete(DeleteView):
    model = ClientePF
    success_url = reverse_lazy('banco:index')


class ClientePJCreate(CreateView):
    model = ClientePJ
    fields = ['nome', 'endereco', 'agencia', 'CNPJ']


class ClientePJUpdate(UpdateView):
    model = ClientePJ
    fields = ['nome', 'endereco', 'agencia', 'CNPJ']


class ClientePJDelete(DeleteView):
    model = ClientePJ
    success_url = reverse_lazy('banco:index')


class Cad_ClienteView(generic.View):
    template_name = 'banco_unisul/cad_cliente.html'

    def get(self, request):
        if not self.request.user.is_authenticated():
            return render(self.request, 'banco_unisul/login.html')
        else:
            return render(self.request, 'banco_unisul/cad_cliente.html')


class Cad_ContaView(generic.View):
    template_name = 'banco_unisul/cad_conta.html'


class Cad_SocioView(generic.View):
    template_name = 'banco_unisul/cad_socio.html'


class RelatorioView(generic.View):
    template_name = 'banco_unisul/relatorio.html'
