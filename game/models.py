import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max


class Parameter(models.Model):
    name = models.CharField(max_length=40)
    unit = models.CharField(max_length=10, blank=True)
    decimals = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Country(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=40)

    # parameters = models.ManyToManyField(Parameter, through="CountryParameter")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "countries"


class CountryParameter(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="parameters")
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="countries")
    value = models.DecimalField(max_digits=20, decimal_places=5)

    def __str__(self):
        return f'{self.country.name} - {self.parameter.name}'

    class Meta:
        ordering = ['parameter', '-value']

    @property
    def formatted_value(self):
        return f'{self.value:0,.{self.parameter.decimals}f} {self.parameter.unit}'


class Championship(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="championships")
    guesses = models.PositiveSmallIntegerField(null=True)
    winner = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="championship_wins", null=True)

    def __str__(self):
        return f'{self.title} (by {self.user})'

    def set_guesses(self):
        n_guesses = 0
        for round in self.rounds.all():
            for match in round.matches.all():
                n_guesses += match.correct_guess()
        self.guesses = n_guesses
        self.save()

    def create_round(self):
        if self.rounds.all().exists():
            countries = []
            prev_round = Round.objects.filter(championship=self.id).latest("number")
            prev_round.process()
            for match in Match.objects.filter(round=prev_round.id):
                countries.extend(list(match.winners.all()))
        else:
            countries = list(Country.objects.all())

        self.set_guesses()

        if len(countries) == 1:
            self.winner = countries[0]
            self.save()
        else:
            parameters = Parameter.objects.filter(active=True)
            round = self.rounds.create(parameter=random.choice(parameters))
            random.shuffle(countries)
            if len(countries) % 2 == 1:
                match = round.matches.create()
                match.countries.add(countries[-1])
                match.winners.add(match.countries.all()[0])
            for a, b in zip(countries[0::2], countries[1::2]):
                match = round.matches.create()
                match.countries.add(a, b)


class Round(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name="rounds")
    number = models.PositiveSmallIntegerField(default=0)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="rounds", null=True)

    def __str__(self):
        return f'Round {self.number}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = 1 + Round.objects.filter(championship=self.championship).aggregate(Max("number", default=0))[
                'number__max']
        return super().save(*args, **kwargs)

    @property
    def is_latest(self):
        return self.number == self.championship.rounds.latest("number").number

    def process(self):
        if self.championship.winner or not self.is_latest:
            return
        for match in self.matches.all():
            match.set_win()


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

    class Meta:
        ordering = ['id']
        verbose_name_plural = "matches"

    @property
    def score(self):
        score_dict = {}
        for country in self.countries.all():
            score_dict[country.id] = CountryParameter.objects.get(country=country.id,
                                                                  parameter=self.round.parameter.id).formatted_value
        return score_dict

    def set_win(self):
        if self.round.championship.winner or not self.round.is_latest:
            return
        max_value = \
            CountryParameter.objects.filter(country__in=self.countries.all(),
                                            parameter=self.round.parameter.id).aggregate(Max("value"))['value__max']
        winning_countries = CountryParameter.objects.filter(country__in=self.countries.all(),
                                                            parameter=self.round.parameter.id,
                                                            value=max_value).values_list('country', flat=True)
        for country in winning_countries:
            self.winners.add(country)

    def correct_guess(self):
        if self.guess in self.winners.all():
            return 1
        return 0
