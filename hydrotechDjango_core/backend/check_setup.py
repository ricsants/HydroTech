import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from usuarios.models import Usuario
from rios.models import Rios, PontoRisco
from datetime import date

def check_setup():
    """Verifica se o setup está correto."""
    print("=" * 60)
    print("VERIFICAÇÃO DO SETUP - HydroTech Backend")
    print("=" * 60)
    
    # 1. Verificar se os modelos estão funcionando
    print("\n✓ Django settings carregadas corretamente")
    
    # 2. Verificar banco de dados
    try:
        usuarios_count = Usuario.objects.count()
        print(f"✓ Banco de dados acessível ({usuarios_count} usuários)")
    except Exception as e:
        print(f"✗ Erro ao acessar banco de dados: {e}")
        return False
    
    # 3. Tentar criar um usuário de teste
    try:
        test_user = Usuario.objects.filter(email='test@example.com').first()
        if not test_user:
            test_user = Usuario.objects.create(
                nome='Usuário Teste',
                email='test@example.com',
                data_nascimento=date(2000, 1, 1)
            )
            test_user.set_password('TestPassword123')
            test_user.save()
            print("✓ Usuário de teste criado com sucesso")
        else:
            print("✓ Usuário de teste já existe")
    except Exception as e:
        print(f"✗ Erro ao criar usuário de teste: {e}")
        return False
    
    # 4. Verificar se os tokens são gerados
    try:
        if not test_user.token:
            test_user.token = test_user.generate_token()
            test_user.save()
        print(f"✓ Token gerado: {test_user.token[:20]}...")
    except Exception as e:
        print(f"✗ Erro ao gerar token: {e}")
        return False
    
    # 5. Verificar se a senha está sendo hasheada
    try:
        if test_user.check_password('TestPassword123'):
            print("✓ Sistema de senha funcionando corretamente")
        else:
            print("✗ Erro ao verificar senha")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar senha: {e}")
        return False
    
    # 6. Tentar criar um rio de teste
    try:
        test_rio = Rios.objects.filter(nome='Rio Teste').first()
        if not test_rio:
            test_rio = Rios.objects.create(
                nome='Rio Teste',
                cidade='São Paulo',
                estado='SP',
                risco_inundacao=2,
                criado_por=test_user
            )
            print("✓ Rio de teste criado com sucesso")
        else:
            print("✓ Rio de teste já existe")
    except Exception as e:
        print(f"✗ Erro ao criar rio: {e}")
        return False
    
    # 7. Tentar criar um ponto de risco
    try:
        test_ponto = PontoRisco.objects.filter(rio=test_rio).first()
        if not test_ponto:
            test_ponto = PontoRisco.objects.create(
                rio=test_rio,
                latitude=-23.5505,
                longitude=-46.6333,
                descricao='Ponto de risco teste para validação do sistema',
                nivel_risco=2,
                criado_por=test_user
            )
            print("✓ Ponto de risco criado com sucesso")
        else:
            print("✓ Ponto de risco já existe")
    except Exception as e:
        print(f"✗ Erro ao criar ponto de risco: {e}")
        return False
    
    # 8. Verificar favoritos
    try:
        test_user.favoritos.add(test_rio)
        if test_user.favoritos.filter(pk=test_rio.pk).exists():
            print("✓ Sistema de favoritos funcionando corretamente")
        else:
            print("✗ Erro ao adicionar favorito")
            return False
    except Exception as e:
        print(f"✗ Erro com sistema de favoritos: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ SETUP VERIFICADO COM SUCESSO!")
    print("=" * 60)
    print("\nO backend está pronto para uso.")
    print("\nCom Docker Compose:")
    print("  docker-compose up -d")
    print("\nSem Docker (desenvolvimento):")
    print("  python manage.py runserver")
    print("\nPara acessar o admin:")
    print("  http://localhost:8000/admin")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = check_setup()
    exit(0 if success else 1)
