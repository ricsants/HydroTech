#!/bin/bash
# Quick Commands - HydroTech Backend

# ============================================
# Development Commands
# ============================================

# Setup inicial
setup_dev() {
    echo "🚀 Iniciando setup de desenvolvimento..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    echo "✓ Setup concluído!"
    echo "Execute: python manage.py runserver"
}

# Migrations
make_migrations() {
    python manage.py makemigrations
    echo "✓ Migrações criadas"
}

apply_migrations() {
    python manage.py migrate
    echo "✓ Migrações aplicadas"
}

# Tests
run_tests() {
    python manage.py test
}

# Check setup
check() {
    python check_setup.py
}

# ============================================
# Docker Commands
# ============================================

docker_build() {
    echo "🐳 Building Docker image..."
    docker-compose build
}

docker_up() {
    echo "🐳 Starting containers..."
    docker-compose up -d
    echo "✓ Containers iniciados"
    echo "Aguarde alguns segundos..."
    sleep 3
}

docker_down() {
    echo "🐳 Parando containers..."
    docker-compose down
}

docker_logs() {
    docker-compose logs -f web
}

docker_shell() {
    docker-compose exec web bash
}

docker_migrate() {
    docker-compose exec web python manage.py migrate
    echo "✓ Migrações aplicadas"
}

docker_check() {
    docker-compose exec web python check_setup.py
}

# ============================================
# Database Commands
# ============================================

reset_db() {
    echo "⚠️  Resetting database..."
    python manage.py flush --no-input
    python manage.py migrate
    echo "✓ Database reset"
}

# ============================================
# Admin Commands
# ============================================

create_superuser() {
    python manage.py createsuperuser
}

# ============================================
# Utility Commands
# ============================================

# Collect static files
collect_static() {
    python manage.py collectstatic --noinput
    echo "✓ Static files collected"
}

# Shell interativo
shell() {
    python manage.py shell
}

# ============================================
# Help
# ============================================

show_help() {
    cat << EOF
HydroTech Backend - Quick Commands

Development:
  ./commands.sh setup_dev          - Setup inicial
  ./commands.sh make_migrations    - Criar migrações
  ./commands.sh apply_migrations   - Aplicar migrações
  ./commands.sh run_tests          - Rodar testes
  ./commands.sh check              - Verificar setup
  ./commands.sh shell              - Shell interativo

Docker:
  ./commands.sh docker_build       - Build imagem
  ./commands.sh docker_up          - Iniciar containers
  ./commands.sh docker_down        - Parar containers
  ./commands.sh docker_logs        - Ver logs
  ./commands.sh docker_shell       - Shell no container
  ./commands.sh docker_migrate     - Migrations no Docker
  ./commands.sh docker_check       - Check no Docker

Database:
  ./commands.sh reset_db           - Reset banco de dados

Admin:
  ./commands.sh create_superuser   - Criar superuser

Utilities:
  ./commands.sh collect_static     - Coletar arquivos estáticos
  ./commands.sh help               - Esta mensagem

Exemplos:
  ./commands.sh setup_dev          # Setup inicial
  ./commands.sh check              # Verificar se está tudo ok
  ./commands.sh docker_up          # Iniciar com Docker

EOF
}

# ============================================
# Main
# ============================================

case "$1" in
    setup_dev)
        setup_dev
        ;;
    make_migrations)
        make_migrations
        ;;
    apply_migrations)
        apply_migrations
        ;;
    run_tests)
        run_tests
        ;;
    check)
        check
        ;;
    docker_build)
        docker_build
        ;;
    docker_up)
        docker_up
        ;;
    docker_down)
        docker_down
        ;;
    docker_logs)
        docker_logs
        ;;
    docker_shell)
        docker_shell
        ;;
    docker_migrate)
        docker_migrate
        ;;
    docker_check)
        docker_check
        ;;
    reset_db)
        reset_db
        ;;
    create_superuser)
        create_superuser
        ;;
    collect_static)
        collect_static
        ;;
    shell)
        shell
        ;;
    *)
        show_help
        ;;
esac
