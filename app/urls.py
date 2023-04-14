from django.urls import path
from . import views

app_name = 'app';
urlpatterns = [
    path('', views.home, name="home"),
    # URLS RENTEL
    path('app/contacto', views.contacto, name='contacto'),
    path('add_incidencia', views.add_incidencia, name='add-incidencia'),
    path('incidencias', views.all_incidencias, name="mostrar-incidencias"),
    path('filtrar_incidencias', views.filtrar_incidencias, name="filtrar-incidencias"),
    path('buscar-incidencias/', views.buscar_incidencias, name='buscar-incidencias'),
    path('update_incidencia/<incidencia_id>', views.update_incidencia, name='update-incidencia'),
    path('delete_incidencia/<incidencia_id>', views.delete_incidencia, name='delete-incidencia'),
    path('perfil', views.perfil, name='perfil'),
    path('index', views.index, name='index'),
    path('soporte', views.soporte, name='soporte'),
    path('tecnico', views.tecnico, name='tecnico'),
    path('administrador', views.administrador, name='administrador'),
    ]
