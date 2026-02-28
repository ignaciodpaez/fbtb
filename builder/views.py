from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from ._transmarket import *

# Create your views here.

# TODO: add pagination
def build_alineation(request):
    template = loader.get_template('builder/index.html')
    context = {}

    competitions = {k: v for k, v in sorted(competition_map.items(), key=lambda item: item[1])}
    
    context['competitions'] = competitions

    return HttpResponse(template.render(context, request))


def get_clubs_ajax(request):
    template = loader.get_template('builder/clubs_form.html')
    context = {}
    
    competition = request.GET.get('competition', 'GB1')
    season = request.GET.get('season', 2000)
    competitions = {k: v for k, v in sorted(competition_map.items(), key=lambda item: item[1])}

    if competition not in competitions.keys():
        competition = 'GB1'
    
    tm = TransfermarktGateway()
    clubs = tm.get_competition_clubs(competition, int(season))

    context['clubs'] = clubs

    return HttpResponse(template.render(context, request))


def get_competition_nations_ajax(request):
    template = loader.get_template('builder/nations_form.html')
    context = {}
    
    competition = request.GET.get('competition', 'GB1')

    nations = sorted(select_competition_nations(competition))

    context['nations'] = nations

    return HttpResponse(template.render(context, request))


def get_nations_ajax(request):
    template = loader.get_template('builder/nations_form.html')
    context = {}
    
    club = request.GET.get('club', 31)
    
    tm = TransfermarktGateway()
    nations = sorted(tm.get_nations(int(club)))

    context['nations'] = nations

    return HttpResponse(template.render(context, request))


def get_players_ajax(request):
    template = loader.get_template('builder/players.html')
    context = {}
    
    club = request.GET.get('club')
    season_start = request.GET.get('ss', None)
    season_end = request.GET.get('se', None)
    nations = request.GET.getlist('nations')
    
    if club is None:
        league = request.GET.get('competition')
        players = select_competition_players(league, nation=nations)
    else:
        players = select_players(
            int(club), 
            int(season_start) if season_start else None, 
            int(season_end)if season_end else None, 
            nation=nations
        )

    context['players'] = players.sort_values(by='position')

    return HttpResponse(template.render(context, request))