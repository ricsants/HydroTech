import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from usuarios.models import Usuario

user, created = Usuario.objects.get_or_create(
    email='usuario@teste.com',
    defaults={
        'nome': 'Usuario Comum',
        'data_nascimento': '1995-05-15',
        'is_defesa_civil': False
    }
)

user.set_password('usuario123')
user.is_defesa_civil = False
user.save()

print("Usuário comum criado com sucesso!")
