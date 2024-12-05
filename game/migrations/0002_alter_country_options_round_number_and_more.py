# Generated by Django 5.1.2 on 2024-11-08 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='round',
            name='number',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='championship',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='championship_wins', to='game.country'),
        ),
        migrations.AlterField(
            model_name='match',
            name='country2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches2', to='game.country'),
        ),
        migrations.AlterField(
            model_name='match',
            name='guess',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_guesses', to='game.country'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_wins', to='game.country'),
        ),
        migrations.AlterField(
            model_name='round',
            name='parameter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='game.parameter'),
        ),
    ]