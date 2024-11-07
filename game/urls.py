from django.urls import path

from . import views

urlpatterns = [
    path('', views.GamesView.as_view(), name='games.list'),
    path('<int:id>/details/', views.GameDetailView.as_view(), name='games.detail'),
    path('create/', views.GameCreateView.as_view(), name='games.create'),
    path('countries/', views.CountriesView.as_view(), name='countries.list'),
    path('countries/<str:id>/details/', views.CountryDetailView.as_view(), name='countries.detail'),
    path('<int:id>/rounds/create/', views.create_round, name='rounds.create'),
    path('<int:id>/rounds/<int:round_id>/match/create/', views.create_match, name='matches.create'),
]