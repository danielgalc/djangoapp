# Generated by Django 4.1.7 on 2023-04-12 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0007_rename_cliente_usuario'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usuario',
            new_name='Cliente',
        ),
    ]