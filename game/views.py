import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import GameForm
from .models import Championship, Country, Round, Match


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


def create_round(request, id):
    championship = Championship.objects.get(id=id)
    round = Round(championship=championship)
    round.save()
    return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]))


def create_match(request, id, round_id):
    round = Round.objects.get(id=round_id)
    countries = list(Country.objects.all())
    random_countries = random.sample(countries, 2)
    match = Match(round=round, country1=random_countries[0], country2=random_countries[1])
    match.save()
    return HttpResponseRedirect(reverse_lazy('games.detail', args=[id]))
