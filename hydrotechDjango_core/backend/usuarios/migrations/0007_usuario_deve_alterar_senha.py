from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_usuario_alertas'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='deve_alterar_senha',
            field=models.BooleanField(default=False, verbose_name='Deve alterar senha no próximo login'),
        ),
    ]
