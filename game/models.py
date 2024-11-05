from django.contrib.auth.models import User
from django.db import models


class Parameter(models.Model):
    name = models.CharField(max_length=40)
    active = models.BooleanField(default=False)


class Country(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=40)
    parameters = models.ManyToManyField(Parameter, through="CountryParameter")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CountryParameter(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="countries")
    value = models.DecimalField(max_digits=20, decimal_places=5)


class Championship(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="championships")
    guesses = models.PositiveSmallIntegerField(null=True, blank=True)
    winner = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="championship_wins", null=True,
                               blank=True)


class Round(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name="rounds")
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="rounds", null=True, blank=True)


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="matches")
    country1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="matches1")
    country2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="matches2")
    winner = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="match_wins", null=True, blank=True)
    guess = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="match_guesses", null=True, blank=True)
