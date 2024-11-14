from django.urls import path

from . import views

urlpatterns = [
    path('', views.GamesView.as_view(), name='games.list'),
    path('<int:id>/details/', views.GameDetailView.as_view(), name='games.detail'),
    path('create/', views.GameCreateView.as_view(), name='games.create'),
    path('countries/', views.CountriesView.as_view(), name='countries.list'),
    path('countries/<str:id>/details/', views.CountryDetailView.as_view(), name='countries.detail'),
    path('parameters/', views.ParametersView.as_view(), name='parameters.list'),
    path('parameters/<str:id>/details/', views.ParameterDetailView.as_view(), name='parameters.detail'),
    path('<int:id>/rounds/create/', views.create_round, name='rounds.create'),
    path('<int:id>/rounds/<int:round_id>/process/', views.process_round, name='rounds.process'),
    path('<int:id>/match/<int:match_id>/win/<str:country_id>', views.match_win, name='matches.win'),
    path('<int:id>/match/<int:match_id>/guess/<str:country_id>', views.match_guess, name='matches.guess'),
]