# Generated by Django 5.1.2 on 2024-11-05 12:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Championship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('guesses', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='championships', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='championship_wins', to='game.country')),
            ],
        ),
        migrations.CreateModel(
            name='CountryParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=5, max_digits=20)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.country')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='game.parameter')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='parameters',
            field=models.ManyToManyField(through='game.CountryParameter', to='game.parameter'),
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='game.championship')),
                ('parameter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='game.parameter')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches1', to='game.country')),
                ('country2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches2', to='game.country')),
                ('guess', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_guesses', to='game.country')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_wins', to='game.country')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='game.round')),
            ],
        ),
    ]
