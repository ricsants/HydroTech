from django.contrib import admin
from .models import Rios, PontoRisco


class RiosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'criado_por')
    list_filter = ('estado',)
    search_fields = ('nome', 'cidade')
    readonly_fields = ('criado_por',)


class PontoRiscoAdmin(admin.ModelAdmin):
    list_display = ('rio', 'latitude', 'longitude', 'criado_por', 'criado_em')
    list_filter = ('rio', 'criado_em')
    search_fields = ('rio__nome', 'descricao')
    readonly_fields = ('criado_por', 'criado_em', 'atualizado_em')


admin.site.register(Rios, RiosAdmin)
admin.site.register(PontoRisco, PontoRiscoAdmin)

