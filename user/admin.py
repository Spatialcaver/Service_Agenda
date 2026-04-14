from django.contrib import admin
from .models import User, Funcionario, AusenciaFuncionario

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'tipo_usuario')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'estabelecimento')
    list_filter = ('estabelecimento',)
    search_fields = ('user__email', 'user__full_name')
    ordering = ('user',)


class AusenciaFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'funcionario', 'data', 'hora_inicio', 'hora_fim', 'motivo')
    list_filter = ('data', 'motivo', 'funcionario__estabelecimento')
    search_fields = ('funcionario__user__full_name', 'funcionario__user__email')
    ordering = ('-data', '-hora_inicio')

admin.site.register(AusenciaFuncionario, AusenciaFuncionarioAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
