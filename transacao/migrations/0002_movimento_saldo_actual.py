# Generated by Django 3.2.4 on 2021-06-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='saldo_actual',
            field=models.FloatField(null=True),
        ),
    ]
