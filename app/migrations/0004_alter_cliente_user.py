# Generated by Django 4.1.7 on 2023-04-11 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_cliente_username_cliente_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
