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
    competitions = {k: v for k, v in sorted(competition_map.items(), key=lambda item: item[1])}

    if competition not in competitions.keys():
        competition = 'GB1'
    
    tm = TransfermarktGateway()
    clubs = tm.get_competition_clubs(competition, 2007)

    context['clubs'] = clubs

    return HttpResponse(template.render(context, request))


def get_nations_ajax(request):
    template = loader.get_template('builder/nations_form.html')
    context = {}
    
    club = request.GET.get('club', 'GB1')
    
    tm = TransfermarktGateway()
    nations = tm.get_nations(club)

    context['nations'] = nations

    return HttpResponse(template.render(context, request))