from django.conf.urls import url
from superadmin import views


urlpatterns = [
    url(r'^$', views.inicio_superadmin, name='superadmin'),
    url(r'^gestor_grupo_alimentos/$', views.gestor_grupos_aliemntos, name='gestor-grupo-alimentos'),
    url(r'^gestor_alimentos/$', views.gestor_aliemntos, name='gestor-alimentos'),
    url(r'^grupo-alimentos-json$', views.grupoAlimentosJson, name='grupo-alimentos-json'),
    
]
