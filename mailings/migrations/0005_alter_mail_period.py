# Generated by Django 4.2.2 on 2024-06-18 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0004_log_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='period',
            field=models.CharField(choices=[('DAILY', 'Раз в день'), ('WEEKLY', 'Раз в неделю'), ('MONTHLY', 'Раз в месяц')], max_length=30, verbose_name='Периодичность'),
        ),
    ]
