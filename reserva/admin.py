from django.contrib import admin
from .models import Reserva


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'cliente', 'telefone', 'servico', 'estabelecimento', 'funcionario')
    list_filter = ('data', 'hora', 'servico', 'estabelecimento', 'funcionario')
    search_fields = ('cliente', 'telefone', 'servico', 'estabelecimento', 'funcionario')
    ordering = ('data', 'hora')
    
admin.site.register(Reserva, ReservaAdmin)