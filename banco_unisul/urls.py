"""sistema_banco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

app_name = 'banco_unisul'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^detalhepf/(?P<pk>[0-9]+)/$', views.DetalhepfView.as_view(), name='detalhepf'),
    url(r'^detalhepj/(?P<pk>[0-9]+)/$', views.DetalhepjView.as_view(), name='detalhepj'),
    url(r'^todoscliente/$', views.TodosClientesView.as_view(), name='todoscliente'),
    url(r'^todosclientepj/$', views.TodosClientesPJView.as_view(), name='todosclientepj'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^cad_cliente/$', views.Cad_ClienteView.as_view(), name='cad_cliente'),
    url(r'^cad_cliente/novaconta/(?P<pk>[0-9]+)/$', views.Conta_ClienteView.as_view(), name='conta_cliente'),
    url(r'^cad_empresa/novosocio/(?P<pk>[0-9]+)/$', views.EmpresaSocioView.as_view(), name='empresa_socio'),
    url(r'^cad_conta/$', views.Cad_ContaView.as_view(), name='cad_conta'),
    url(r'^detalheconta/(?P<pk>[0-9]+)/$', views.DetalheContaView.as_view(), name='detalheconta'),
    url(r'^listaconta/$', views.ListaContaView.as_view(), name='listaconta'),
    url(r'^listaexcluiconta/$', views.ContaExclusao.as_view(), name='listaexcluiconta'),
    url(r'^listaexcluiclientepf/$', views.ListaPFExclusao.as_view(), name='listaexcluiclientepf'),
    url(r'^listaexcluiclientepj/$', views.ListaPJExclusao.as_view(), name='listaexcluiclientepj'),
    url(r'^dadosrelatorio/$', views.DadosRelatorioView.as_view(), name='dadosrelatorio'),
    url(r'^novaconta/$', views.ContaCreate.as_view(), name='novaconta'),
    url(r'^saldoclientes/$', views.SaldoClientesView.as_view(), name='saldoclientes'),
    url(r'^totalcontas/$', views.TotalContasView.as_view(), name='totalcontas'),


    url(r'^cad_socio/$', views.Cad_SocioView.as_view(), name='cad_socio'),
    url(r'^alt_socio/$', views.SocioUpdate.as_view(), name='alt_socio'),
    url(r'^listaclientespjexclui/$', views.SocioExclusao.as_view(), name='listaclientespjexclui'),

    url(r'^relatorio/$', views.RelatorioView.as_view(), name='relatorio'),

    url(r'^alteraclientepf/$', views.AlteraClientePF.as_view(), name='alteraclientepf'),
    url(r'^alteraclientepj/$', views.AlteraClientePJ.as_view(), name='alteraclientepj'),

    url(r'^saque/$', views.SaqueListView.as_view(), name='saque'),
    url(r'^transferencia/$', views.TransferenciaListView.as_view(), name='transferencia'),
    url(r'^deposito/$', views.DepositoListView.as_view(), name='deposito'),

    url(r'^clientepf/novo/$', views.ClientePFCreate.as_view(), name='clientepf-add'),
    url(r'^clientepj/novo/$', views.ClientePJCreate.as_view(), name='clientepj-add'),
    url(r'^saque/(?P<pk>[0-9]+)/$', views.SaqueView.as_view(), name='saque-add'),
    url(r'^transferencia/(?P<pk>[0-9]+)/$', views.TransferenciaView.as_view(), name='transferencia-add'),
    url(r'^deposito/(?P<pk>[0-9]+)/$', views.DepositoView.as_view(), name='deposito-add'),
    url(r'^cad_socio/novo/$', views.SocioView.as_view(), name='socio-add'),
    url(r'^cad_conta/novo/(?P<pk>[0-9]+)/$', views.ContaCreate.as_view(), name='conta-add'),

    url(r'^clientepf/(?P<pk>[0-9]+)/$', views.ClientePFUpdate.as_view(), name='clientepf-update'),
    url(r'^clientepj/(?P<pk>[0-9]+)/$', views.ClientePJUpdate.as_view(), name='clientepj-update'),
    url(r'^alt_conta/(?P<pk>[0-9]+)/$', views.ContaUpdate.as_view(), name='conta-update'),

    url(r'^clientepf/(?P<pk>[0-9]+)/delete/$', views.ClientePFDelete.as_view(), name='clientepf-delete'),
    url(r'^clientepj/(?P<pk>[0-9]+)/delete/$', views.ClientePJDelete.as_view(), name='clientepj-delete'),
    url(r'^exc_socio/(?P<pk>[0-9]+)/delete/$', views.SocioDelete.as_view(), name='exc_socio-delete'),
    url(r'^exc_conta/(?P<pk>[0-9]+)/delete/$', views.ContaDelete.as_view(), name='exc_conta-delete'),
]
