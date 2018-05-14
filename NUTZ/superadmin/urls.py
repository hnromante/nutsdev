from django.conf.urls import url
from superadmin import views


urlpatterns = [
    url(r'^$', views.inicio_superadmin, name='superadmin'),

    
]
