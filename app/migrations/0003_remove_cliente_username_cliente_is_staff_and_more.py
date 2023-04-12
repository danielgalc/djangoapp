# Generated by Django 4.1.7 on 2023-04-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cliente_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='username',
        ),
        migrations.AddField(
            model_name='cliente',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cliente',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='password',
            field=models.CharField(default=None, max_length=20),
        ),
    ]