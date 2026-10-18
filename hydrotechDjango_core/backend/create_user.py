"""Cria uma conta local de demonstração somente com credenciais fornecidas no ambiente."""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from usuarios.models import Usuario


def main():
    email = os.getenv('DEMO_EMAIL', '').strip()
    password = os.getenv('DEMO_PASSWORD', '')
    if not email or not password:
        print('Conta não criada: configure DEMO_EMAIL e DEMO_PASSWORD no ambiente.')
        return

    if Usuario.objects.filter(email=email).exists():
        print('Conta de demonstração já existe; nenhuma senha foi alterada.')
        return

    user = Usuario(
        email=email,
        nome=os.getenv('DEMO_NOME', 'Usuário de Demonstração'),
        data_nascimento='2000-01-01',
        is_defesa_civil=False,
    )
    user.set_password(password)
    user.save()
    print('Conta de demonstração criada sem permissão administrativa.')


if __name__ == '__main__':
    main()
