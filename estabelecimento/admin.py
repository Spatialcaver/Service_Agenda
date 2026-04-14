from django.contrib import admin
from .models import Estabelecimento, Servicos, Funcionamento

class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'proprietario__full_name', 'endereco')
    list_filter = ('proprietario',)
    search_fields = ('nome', 'proprietario__full_name', 'endereco')
    ordering = ('nome',)
    filter_horizontal = ('dia_funcionamento', 'servicos_oferecidos')

class ServicosAdmin(admin.ModelAdmin):
    list_display = ('servico', 'duracao', 'preco', 'estabelecimento__nome', 'responsavel__full_name')
    list_filter = ('estabelecimento__nome', 'responsavel__full_name')
    search_fields = ('servico', 'estabelecimento__nome', 'responsavel__username', 'responsavel__first_name', 'responsavel__last_name', 'responsavel__email')
    ordering = ('servico',)

class FuncionamentoAdmin(admin.ModelAdmin):
    list_display = ('dia', 'horario_abertura', 'horario_fechamento')
    list_filter = ('dia', )
    search_fields = ('dia',)
    ordering = ('dia',)
  
admin.site.register(Funcionamento, FuncionamentoAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Servicos, ServicosAdmin)
