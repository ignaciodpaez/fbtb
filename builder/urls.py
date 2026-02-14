from django.urls import path

from . import views

urlpatterns = [
    path("", views.build_alineation, name="index"),
    path("ajax/clubs", views.get_clubs_ajax, name="ajax_clubs"),
]