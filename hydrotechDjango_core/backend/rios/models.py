from django.db import models

class Rios(models.Model):
    
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    criado_por = models.ForeignKey('usuarios.Usuario', null=True, blank=True, on_delete=models.SET_NULL, related_name='rios')
    descricao_gemini = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome


class PontoRisco(models.Model):
    rio = models.ForeignKey(Rios, on_delete=models.CASCADE, related_name='pontos_risco')
    latitude = models.FloatField()
    longitude = models.FloatField()
    descricao = models.TextField()
    nivel_base = models.FloatField(default=1.0)
    limite_atencao = models.FloatField(default=1.5)
    limite_alerta = models.FloatField(default=2.5)
    limite_emergencia = models.FloatField(default=3.5)
    criado_por = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, related_name='pontos_risco_criados')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ponto de Risco - {self.rio.nome}"
