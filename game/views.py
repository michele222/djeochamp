import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import GameForm
from .models import Championship, Country, Round, Match, Parameter


class GamesView(LoginRequiredMixin, ListView):
    model = Championship
    template_name = 'game/game_list.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return self.request.user.championships.all()


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Championship
    template_name = 'game/game_detail.html'
    login_url = reverse_lazy('login')

    def get_object(self):
        return Championship.objects.get(id=self.kwargs['id'])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["round_list"] = Round.objects.all()
    #     return context


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Championship
    template_name = 'game/game_create.html'
    form_class = GameForm
    success_url = reverse_lazy('games.detail')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('games.detail', args=[self.object.id]))


class CountriesView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'game/country_list.html'
    login_url = reverse_lazy('login')


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country
    template_name = 'game/country_detail.html'
    login_url = reverse_lazy('login')

    def get_object(self):
        return Country.objects.get(id=self.kwargs['id'])


class ParametersView(LoginRequiredMixin, ListView):
    model = Parameter
    template_name = 'game/parameter_list.html'
    login_url = reverse_lazy('login')


class ParameterDetailView(LoginRequiredMixin, DetailView):
    model = Parameter
    template_name = 'game/parameter_detail.html'
    login_url = reverse_lazy('login')

    def get_object(self):
        return Parameter.objects.get(id=self.kwargs['id'])


def create_round(request, id):
    response = HttpResponseRedirect(reverse_lazy('games.detail', args=[id]))
    championship = Championship.objects.get(id=id)
    if championship.winner:
        return response
    if championship.rounds.all().exists():
        countries = []
        prev_round = Round.objects.filter(championship=id).latest("number")
        prev_round.process()
        for match in Match.objects.filter(round=prev_round.id):
            countries.extend(list(match.winners.all()))
    else:
        countries = list(Country.objects.all())

    championship.set_guesses()

    if len(countries) == 1:
        championship.winner = countries[0]
        championship.save()
    else:
        round = Round(championship=championship)
        parameters = Parameter.objects.filter(active=True)
        round.parameter = random.choice(parameters)
        round.save()
        random.shuffle(countries)
        if len(countries) % 2 == 1:
            match = Match(round=round)
            match.save()
            match.countries.add(countries[-1])
            match.winners.add(match.countries.all()[0])
        for a, b in zip(countries[0::2], countries[1::2]):
            match = Match(round=round)
            match.save()
            match.countries.add(a, b)
    return response


def process_round(request, id, round_id):
    round = Round.objects.get(id=round_id)
    round.process()
    return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]))


def match_win(request, id, match_id, country_id):
    match = Match.objects.get(id=match_id)
    if match.round.championship.winner or not match.round.is_latest:
        return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]))
    country = Country.objects.get(id=country_id)
    match.winners.add(country)
    return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]) + f'#match_{match_id}')


def match_guess(request, id, match_id, country_id):
    match = Match.objects.get(id=match_id)
    if match.round.championship.winner or not match.round.is_latest:
        return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]))
    country = Country.objects.get(id=country_id)
    match.guess = country
    match.save()
    return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]) + f'#match_{match_id}')
