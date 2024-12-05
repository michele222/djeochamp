# Generated by Django 5.1.2 on 2024-11-08 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_country_options_round_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='country1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='country2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner',
        ),
        migrations.AddField(
            model_name='match',
            name='countries',
            field=models.ManyToManyField(related_name='match_plays', to='game.country'),
        ),
        migrations.AddField(
            model_name='match',
            name='winners',
            field=models.ManyToManyField(null=True, related_name='match_wins', to='game.country'),
        ),
    ]