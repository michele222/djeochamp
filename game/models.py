from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max


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
    winner = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="championship_wins", null=True)


class Round(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name="rounds")
    number = models.PositiveSmallIntegerField()
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="rounds", null=True)

    def __str__(self):
        return f'Round {self.number}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = 1 + Round.objects.filter(championship=self.championship).aggregate(Max("number", default=0))['number__max']
        return super().save(*args, **kwargs)

class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="matches")
    countries = models.ManyToManyField(Country, related_name="match_plays")
    winners = models.ManyToManyField(Country, related_name="match_wins")
    guess = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="match_guesses", null=True)

    def __str__(self):
        num_countries = self.countries.count()
        if num_countries == 0:
            return 'empty match'
        if num_countries == 1:
            return f'{self.countries.all()[0].name} - BYE'
        return f'{self.countries.all()[0].name} - {self.countries.all()[1].name}'
