from django.db import models
from django.contrib.auth.hashers import check_password
import secrets

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    senha = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_nascimento = models.DateField()
    token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    api_token = models.CharField(max_length=64, blank=True, null=True, unique=True, verbose_name='API Token')
    favoritos = models.ManyToManyField('rios.PontoRisco', blank=True, related_name='favorited_by')
    alertas = models.ManyToManyField('rios.PontoRisco', blank=True, related_name='alerted_by')
    is_defesa_civil = models.BooleanField(default=False, verbose_name='É Defesa Civil')
    telefone = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='Telefone')
    deve_alterar_senha = models.BooleanField(default=False, verbose_name='Deve alterar senha no próximo login')

    def __str__(self):
        return self.nome or self.email or self.telefone or 'Usuário'

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        if not self.senha:
            return False
        if self.senha.startswith('pbkdf2_') or self.senha.startswith('argon2$') or self.senha.startswith('bcrypt_sha256$'):
            return check_password(raw_password, self.senha)
        return self.senha == raw_password

    def generate_token(self):
        token = secrets.token_urlsafe(32)
        while Usuario.objects.filter(token=token).exists():
            token = secrets.token_urlsafe(32)
        return token

    def generate_api_token(self):
        api_token = secrets.token_urlsafe(32)
        while Usuario.objects.filter(api_token=api_token).exists():
            api_token = secrets.token_urlsafe(32)
        return api_token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)