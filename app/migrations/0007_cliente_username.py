# Generated by Django 4.1.7 on 2023-03-31 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_cliente_incidencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='username',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
