# Generated by Django 5.1.2 on 2024-11-14 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_parameter_unit_alter_championship_guesses'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name_plural': 'countries'},
        ),
        migrations.AlterModelOptions(
            name='countryparameter',
            options={'ordering': ['parameter', '-value']},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['id'], 'verbose_name_plural': 'matches'},
        ),
        migrations.AddField(
            model_name='parameter',
            name='decimals',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
