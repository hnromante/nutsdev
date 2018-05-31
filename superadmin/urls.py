from django.conf.urls import url
from superadmin import views


urlpatterns = [
    url(r'^$', views.inicio_superadmin, name='superadmin'),
    url(r'^grupo-alimentos-json$', views.grupoAlimentosJson, name='grupo-alimentos-json'),
    
]
