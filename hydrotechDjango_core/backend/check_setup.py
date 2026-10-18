"""Diagnóstico local sem criar usuários nem modificar o banco de dados."""
import os

import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from rios.models import PontoRisco, Rios
from usuarios.models import Usuario


def main():
    call_command('check')
    try:
        print('Banco acessível.')
        print('Usuários cadastrados:', Usuario.objects.count())
        print('Rios cadastrados:', Rios.objects.count())
        print('Pontos de risco cadastrados:', PontoRisco.objects.count())
    except Exception as error:
        print('Não foi possível consultar o banco:', error)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
