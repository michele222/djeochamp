from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Championship


class GamesView(LoginRequiredMixin, ListView):
    model = Championship
    template_name = 'game/games_list.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return self.request.user.championships.all()

class GamesDetailView(LoginRequiredMixin, DetailView):
    model = Championship
    template_name = 'game/games_detail.html'
    login_url = reverse_lazy('login')