# Generated by Django 3.2.10 on 2022-06-17 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='public_e_sign_key',
            field=models.CharField(default='test', max_length=350),
        ),
    ]
