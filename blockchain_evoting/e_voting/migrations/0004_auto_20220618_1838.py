# Generated by Django 3.2.9 on 2022-06-18 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_voting', '0003_alter_voter_public_e_sign_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='public_e_sign_key',
            field=models.CharField(default=b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDSs0oam3dP16wP8Sgso3/P39EW\nkSPP8M1tQE1DqnVYeab8SWsB5nORF/YLKwMFBX1vTRjvw+ikdZ3tYZu/dx8LhqnE\nU/a5yTOMULWFOHDrrD40U1OcIAOqWcevp5HeSKAX8b/NBeS31SvQYJzk4fK0v3Gw\nX7OqdaDOJ1OciCvTeQIDAQAB\n-----END PUBLIC KEY-----', max_length=350),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('voter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='e_voting.voter')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_voting.candidate')),
            ],
        ),
    ]
