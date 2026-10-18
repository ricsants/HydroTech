from django.contrib import admin
from .models import Sensor, SensorGroup, Leitura


class SensorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'unidade', 'status', 'grupo', 'rio', 'atualizado_em')
    list_filter = ('tipo', 'status', 'grupo', 'rio')
    search_fields = ('nome', 'modelo', 'grupo__nome')


class SensorGroupAdmin(admin.ModelAdmin):
    list_display = ('nome', 'parent', 'rio', 'endereco', 'get_total_sensores')
    list_filter = ('rio', 'parent')
    search_fields = ('nome', 'descricao', 'endereco')

    @admin.display(description='Total de sensores')
    def get_total_sensores(self, obj):
        return obj.get_total_sensores()


class LeituraAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'valor', 'criado_em')
    list_filter = ('sensor', 'criado_em')


admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorGroup, SensorGroupAdmin)
admin.site.register(Leitura, LeituraAdmin)