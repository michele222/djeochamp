from django.urls import path

from . import views

urlpatterns = [
    path('', views.GamesView.as_view(), name='games.list'),
    path('<int:id>/details/', views.GamesDetailView.as_view(), name='games.detail'),
]