from django.contrib import admin
from .models import Cliente, Incidencia, Venue
from .models import MyClubUser
from .models import Event

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
    list_display = ('titulo_incidencia', 'fecha', 'direccion')
    list_filter = ('fecha', 'direccion')
    ordering = ('-fecha',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    fields = ('email', 'nombre', 'apellido', 'dni', 'tlf', 'direccion')
    list_display = ('email', 'direccion')
    list_filter = ('email', 'direccion')
    ordering = ('email',)





