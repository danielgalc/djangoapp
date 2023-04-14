from django.contrib import admin
from .models import Incidencia, Venue
from .models import MyClubUser
from .models import Event
from app.models import *

#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name','address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)

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





