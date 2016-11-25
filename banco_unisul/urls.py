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

    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^cad_cliente/$', views.Cad_ClienteView.as_view(), name='cad_cliente'),
    url(r'^cad_conta/$', views.Cad_ContaView.as_view(), name='cad_conta'),
    url(r'^cad_socio/$', views.Cad_SocioView.as_view(), name='cad_socio'),
    url(r'^relatorio/$', views.RelatorioView.as_view(), name='relatorio'),

    url(r'clientepf/novo/$', views.ClientePFCreate.as_view(), name='clientepf-add'),
    url(r'clientepj/novo/$', views.ClientePJCreate.as_view(), name='clientepj-add'),

    url(r'clientepf/(?P<pk>[0-9]+)/$', views.ClientePFUpdate.as_view(), name='clientepf-update'),
    url(r'clientepj/(?P<pk>[0-9]+)/$', views.ClientePJUpdate.as_view(), name='clientepj-update'),

    url(r'clientepf/(?P<pk>[0-9]+)/delete/$', views.ClientePFDelete.as_view(), name='clientepf-delete'),
    url(r'clientepj/(?P<pk>[0-9]+)/delete/$', views.ClientePJDelete.as_view(), name='clientepj-delete'),
]
