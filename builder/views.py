from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json

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
    season = request.GET.get('ss', 2000)
    competitions = {k: v for k, v in sorted(competition_map.items(), key=lambda item: item[1])}

    if competition not in competitions.keys():
        competition = 'GB1'
    
    tm = TransfermarktGateway()
    clubs = tm.get_competition_clubs(competition, get_int_param(season, 2000))

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
    sql = request.GET.get('sql', None)
    
    if sql:
        players = read_sql_query(pd.read_csv('data/tm_players.csv'), 'tm_players', sql)
    elif club is None:
        league = request.GET.get('competition')
        players = select_competition_players(league, nation=nations)
    else:
        players = select_players(
            int(club), 
            int(season_start) if season_start else None, 
            int(season_end)if season_end else None, 
            nation=nations
        )

    players['age'] = pd.to_numeric(players['age'], downcast='integer')
    players['height'] = pd.to_numeric(players['height'], downcast='integer')

    context['players'] = players.sort_values(by='position')

    return HttpResponse(template.render(context, request))


@csrf_exempt
def save_squad_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            save_user_squad(data['name'], data['players'])
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
    
    return HttpResponseBadRequest("Only POST allowed")


def find_squad_ajax(request):
    template = loader.get_template('builder/squad_list.html')
    context = {}
    
    name = request.GET.get('squad_name')
    timestamp = request.GET.get('timestamp')

    squad = select_user_squad(name, timestamp) #.drop_duplicates(subset=['squad_name', 'timestamp'], keep='first')
    grouped_df = squad.groupby(['timestamp', 'squad_name']).size().reset_index(name='size')

    context['squad_list'] = grouped_df

    return HttpResponse(template.render(context, request))

def show_squad_ajax(request):
    template = loader.get_template('builder/players.html')
    context = {}
    
    name = request.GET.get('squad_name')
    timestamp = request.GET.get('timestamp')

    squad = select_user_squad(name, int(timestamp))

    context['players'] = squad

    return HttpResponse(template.render(context, request))