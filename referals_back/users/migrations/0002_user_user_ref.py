# Generated by Django 4.2.4 on 2023-08-07 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_ref',
            field=models.CharField(default='DevQUV', editable=False, max_length=6, unique=True, verbose_name='Porsonal reference'),
        ),
    ]
