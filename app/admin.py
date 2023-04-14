from django.contrib import admin
from .models import Incidencia
from app.models import *

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    fields = ('titulo_incidencia', 'desc_incidencia', 'fecha', 'asignada', 'direccion', 'cliente_id')
    list_display = ('titulo_incidencia', 'fecha', 'direccion', 'cliente_id')
    list_filter = ('fecha', 'direccion')
    ordering = ('-fecha',)

    readonly_fields = ['fecha']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    #Si en fields colocamos PASSWORD estamos obligados a escribirla y no se va a cifrar.
    fields = ('email', 'nombre', 'apellido', 'rol', 'dni', 'tlf', 'direccion')
    list_display = ('email', 'rol', 'direccion')
    list_filter = ('email', 'rol', 'direccion')
    ordering = ('email',)





