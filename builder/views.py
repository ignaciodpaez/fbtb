from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from _transmarket import *

# Create your views here.

def build_alineation(request):
    template = loader.get_template('builder/index.html')
    context = {}
    
    competition = request.GET.get('c', 'GB1')
    competitions = {k: v for k, v in sorted(competition_map.items(), key=lambda item: item[1])}

    if competition not in competitions.keys():
        competition = 'GB1'

    if request.GET.get('action') == 'getclubs':
        context = handle_get_clubs(context, competitions, comp)
    elif request.GET.get('action') == 'search':
        template = loader.get_template('teams/players.html')
        context = handle_search_players(request, context, competitions, comp)
    elif request.GET.get('action') == 'getnations':
        template = loader.get_template('teams/nations.html')
        context = handle_get_nations(request, context, competitions, comp)
    else:
        context = handle_get_clubs(context, competitions, comp)

    # add pagination

    return HttpResponse(template.render(context, request))