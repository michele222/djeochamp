# Generated by Django 5.1.2 on 2024-11-29 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_country_options_alter_countryparameter_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='parameters',
        ),
        migrations.AlterField(
            model_name='countryparameter',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='game.country'),
        ),
    ]
