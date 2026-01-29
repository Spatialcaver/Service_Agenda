from django.contrib import admin
from .models import Estabelecimento, Servicos

class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'proprietario', 'endereco', 'horario_abertura', 'horario_fechamento', 'dia_funcionamento')
    list_filter = ('proprietario', 'dia_funcionamento')
    search_fields = ('nome', 'endereco', 'proprietario__username', 'proprietario__first_name', 'proprietario__last_name', 'proprietario__email')
    ordering = ('nome',)

class ServicosAdmin(admin.ModelAdmin):
    list_display = ('servico', 'duracao', 'preco', 'estabelecimento', 'responsavel')
    list_filter = ('estabelecimento', 'responsavel')
    search_fields = ('servico', 'estabelecimento__nome', 'responsavel__username', 'responsavel__first_name', 'responsavel__last_name', 'responsavel__email')
    ordering = ('servico',)

admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Servicos, ServicosAdmin)
