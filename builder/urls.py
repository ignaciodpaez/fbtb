from django.urls import path

from . import views

urlpatterns = [
    path("", views.build_alineation, name="index"),
    path("ajax/clubs", views.get_clubs_ajax, name="ajax_clubs"),
    path("ajax/comp/nations", views.get_competition_nations_ajax, name="ajax_comp_nations"),
    path("ajax/nations", views.get_nations_ajax, name="ajax_nations"),
    path("ajax/players", views.get_players_ajax, name="ajax_players"),
]