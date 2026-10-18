import os
import logging
from django.core.management.base import BaseCommand
from usuarios.models import Usuario

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Cria o usuário admin padrão (Defesa Civil) se não existir'

    def handle(self, *args, **options):
        email = os.getenv('ADMIN_EMAIL', '').strip()
        senha = os.getenv('ADMIN_PASSWORD', '')
        nome = os.getenv('ADMIN_NOME', 'Administrador HydroTech')

        if not email or not senha:
            self.stdout.write(self.style.WARNING('Admin não criado: configure ADMIN_EMAIL e ADMIN_PASSWORD no ambiente.'))
            return

        if Usuario.objects.filter(email=email).exists():
            self.stdout.write(self.style.SUCCESS(f'Admin já existe: {email}'))
            return

        Usuario.objects.create(
            nome=nome,
            email=email,
            data_nascimento='2000-01-01',
            is_defesa_civil=True,
            deve_alterar_senha=True,
        )
        user = Usuario.objects.get(email=email)
        user.set_password(senha)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Admin criado: {email}'))
