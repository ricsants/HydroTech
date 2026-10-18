import json
import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from .models import Usuario


class PermissoesCadastroPublicoTest(TestCase):
    def test_cadastro_e_perfil_nao_concedem_permissao_de_defesa_civil(self):
        cadastro = self.client.post(
            '/auth/register/',
            data=json.dumps({
                'nome': 'Pessoa de Teste',
                'email': 'pessoa@example.invalid',
                'data_nascimento': '2000-01-01',
                'senha': 'SenhaLocal123',
                'is_defesa_civil': True,
            }),
            content_type='application/json',
        )
        self.assertEqual(cadastro.status_code, 201)
        usuario = Usuario.objects.get(email='pessoa@example.invalid')
        self.assertFalse(usuario.is_defesa_civil)

        perfil = self.client.patch(
            '/auth/me/',
            data=json.dumps({'is_defesa_civil': True}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {cadastro.json()['access']}",
        )
        self.assertEqual(perfil.status_code, 200)
        usuario.refresh_from_db()
        self.assertFalse(usuario.is_defesa_civil)

    def test_seed_admin_sem_credenciais_nao_cria_conta(self):
        with patch.dict(os.environ, {'ADMIN_EMAIL': '', 'ADMIN_PASSWORD': ''}):
            call_command('seed_admin', stdout=StringIO())
        self.assertFalse(Usuario.objects.filter(is_defesa_civil=True).exists())
