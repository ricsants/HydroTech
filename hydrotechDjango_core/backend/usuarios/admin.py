from django.contrib import admin
from .models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'is_defesa_civil', 'data_criacao', 'has_api_token')
    list_filter = ('data_criacao', 'is_defesa_civil')
    search_fields = ('nome', 'email')
    readonly_fields = ('data_criacao', 'token', 'api_token')
    fields = ('nome', 'email', 'senha', 'data_nascimento', 'is_defesa_civil', 'data_criacao', 'token', 'api_token')
    
    def has_api_token(self, obj):
        return bool(obj.api_token)
    has_api_token.short_description = 'API Token'
    has_api_token.boolean = True
    
    def save_model(self, request, obj, form, change):
        if not obj.api_token:
            obj.api_token = obj.generate_api_token()
        super().save_model(request, obj, form, change)


admin.site.register(Usuario, UsuarioAdmin)

