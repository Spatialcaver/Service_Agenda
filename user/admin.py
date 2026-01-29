from django.contrib import admin
from .models import User, Funcionario

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'tipo_usuario')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'estabelecimento')
    list_filter = ('estabelecimento',)
    search_fields = ('user__email', 'user__full_name')
    ordering = ('user',)

admin.site.register(User, UserAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
