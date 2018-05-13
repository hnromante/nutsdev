
from django.conf.urls import url
from nutricionista import views


urlpatterns = [
    url(r'^$', views.inicio_nutri, name='nutricionista-index'),
    url(r'^dashboard/$', views.PacienteListView.as_view(), name='nutricionista-dashboard'),
    url(r'^alimentos/$', views.AlimentoCreate.as_view(), name='alimentos'),
    url(r'^tipo-alimentos/$', views.TipoAlimentoCreate.as_view(), name='tipo-alimento'),
    url(r'^calculadora/$', views.calculadora, name='nutricionista-calculadora'),
    
]
