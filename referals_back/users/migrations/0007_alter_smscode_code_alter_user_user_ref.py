# Generated by Django 4.2.4 on 2023-08-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_smskey_smscode_rename_key_smscode_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscode',
            name='code',
            field=models.CharField(default='9811', editable=False, max_length=4),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_ref',
            field=models.CharField(default='sUzs7g', editable=False, max_length=6, unique=True, verbose_name='Personal reference'),
        ),
    ]