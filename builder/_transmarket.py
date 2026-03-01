import ast
import concurrent.futures as cf
import json
import os
import sqlite3
import time
import urllib.parse

import requests
import pandas as pd


competition_map = {
    "GB1": "Premier League",
    "ES1": "La Liga",
    "IT1": "Serie A",
    "FR1": "Ligue 1",
    "L1": "Bundesliga",
    "PO1": "Primeira Liga",
    "NL1": "Eredivisie",
    "BRA1": "Campeonato Brasileiro Série A",
    "ARG1": "Primera División Argentina",
    # "CL": "Champions League",
    # "EL": "Europa League",
}


class TransfermarktGateway:

    def build_players_url(self, club_id, season_id):
        return f"http://0.0.0.0:8000/clubs/{club_id}/players?season_id={season_id}"
    
    def build_competition_clubs_url(self, competition_id, season_id=None):
        url = f'http://0.0.0.0:8000/competitions/{competition_id}/clubs'
        if season_id:
            url += f"?season_id={season_id}"
        
        return url
    
    def fetch_players(self, club_id, season_id):
        response = requests.get(
            self.build_players_url(club_id, season_id), headers={"accept": "application/json"}
        )
        if response.status_code != 200:
            raise Exception("Failed to fetch players data");
        return response.json()
    
    def fetch_competition_clubs(self, competition_id, season_id=None):
        response = requests.get(
            self.build_competition_clubs_url(competition_id, season_id), headers={"accept": "application/json"}
        )
        return response.json()
    
    def build_file_name_from_url(self, club_id, season_id):
        url = self.build_players_url(club_id, season_id)
        file_name = (
            urllib.parse.quote(url, safe="").replace("/", "_") + ".csv"
        )
        return f"data/{file_name}"

    def save_players(self, club_id, season_id):
        file_name = f"data/tm_players.csv"
        file_exists = os.path.exists(file_name)
        if file_exists is False:
            raise RuntimeError(f"{file_name} not exists")
        try:
            df = pd.read_csv(file_name)
            df_players = df[(df["club_id"] == club_id) & (df["season_id"] == season_id)]
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()
            df_players = df
        if df_players.empty:
            print(f"Data is empty. Fetching data from API.")
            data = self.fetch_players(club_id, season_id)
            df_players = pd.DataFrame(data['players'])
            df_players['club_id'] = club_id
            df_players['season_id'] = season_id
            # data.to_csv(file_name, mode='a', index=False, header=not file_exists)
            df_final = pd.concat([df, df_players], ignore_index=True, sort=False)
            print(f"Data ({club_id}, {season_id}) saved to {file_name}")
            df_final.to_csv(file_name, index=False)

        return df_players


    def get_competition_clubs(self, competition_id, season_id=None):
        file_name = f"data/tm_clubs.csv"
        file_exists = os.path.exists(file_name)
        if file_exists is False:
            raise RuntimeError(f"{file_name} not exists")
        df = pd.read_csv(file_name)
        df_clubs = df[(df['id'] == competition_id) & (df["seasonId"] == season_id)]

        return df_clubs
    
    def save_competition_clubs(self, competition_id, season_id=None):
        file_name = f"data/tm_clubs.csv"
        file_exists = os.path.exists(file_name)
        if file_exists is False:
            raise RuntimeError(f"{file_name} not exists")
        try:
            df = pd.read_csv(file_name)
            df_clubs = df[(df['id'] == competition_id) & (df["seasonId"] == season_id)]
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()
            df_clubs = df
        if df_clubs.empty:
            print(f"Data is empty. Fetching data from API.")
            data = self.fetch_competition_clubs(competition_id, season_id)
            df_data = pd.DataFrame(data)
            df_norm = pd.json_normalize(df_data['clubs']).add_prefix('club_')
            df_clubs = pd.concat([df_data.drop('clubs', axis=1), df_norm], axis=1)
            df_final = pd.concat([df, df_clubs], ignore_index=True, sort=False)
            print(f"Data ({competition_id}, {season_id}) saved to {file_name}")
            df_final.to_csv(file_name, index=False)

        return df_clubs
    
    def get_players_async(self, club_id, seasons=None, save_to_file=False):

        years = range(1990, 1993) if seasons is None else seasons
        params = [(club_id, i, save_to_file) for i in years]
        results = []

        with cf.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self.get_players, *param): param for param in params}
            for future in cf.as_completed(future_to_url):
                param = future_to_url[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    print('%r generated an exception: %s' % (param, exc))
                else:
                    print('%r page is %d bytes' % (param, len(data)))
        
        return results
    
    def delete_players_file(self, club_id, season_id):
        pass

    def get_nations(self, club_id):
        file_name = f"data/tm_players.csv"
        file_exists = os.path.exists(file_name)
        if file_exists is False:
            raise RuntimeError(f"{file_name} not exists")
        df = pd.read_csv(file_name)
        data = df[df["club_id"] == club_id]['nationality'].unique()
        nations = set()
        for i in data:
            nations.update(ast.literal_eval(i))
        
        return nations
    
    def get_players(self, club_id, nations=[]):
        file_name = f"data/tm_players.csv"
        file_exists = os.path.exists(file_name)
        if file_exists is False:
            raise RuntimeError(f"{file_name} not exists")
        df = pd.read_csv(file_name)
        data = df[df["club_id"] == club_id].drop_duplicates(subset=['id'])
        data['nationality'] = data['nationality'].apply(ast.literal_eval)
        if not nations:
            return data
        exploded = data.explode('nationality')
        mask = exploded['nationality'].isin(nations)
        valids = exploded[mask].index.unique()
        resultado = df.loc[valids]
        
        return resultado


def save_players(club_id, season_start, season_end=None):
    gw = TransfermarktGateway()
    end = season_start if season_end is None else season_end
    years = range(season_start, end + 1)
    for year in years:
        gw.save_players(club_id, year)
        time.sleep(5)


def save_competition_clubs(competition_id, season_start, season_end=None):
    gw = TransfermarktGateway()
    end = season_start if season_end is None else season_end
    years = range(season_start, end + 1)
    for year in years:
        gw.save_competition_clubs(competition_id, year)
        time.sleep(5)


def select_players(club_id, season_start=None, season_end=None, nation=[]):
    df_player = pd.read_csv('data/tm_players.csv')
    df_player['nationality'] = df_player['nationality'].apply(ast.literal_eval)

    df_club = pd.read_csv('data/tm_clubs.csv')

    df_player = pd.merge(df_player, df_club, on='club_id', how='left', suffixes=("", "_y"))

    mask = (df_player['club_id'] == club_id)
    mask &= df_player['nationality'].apply(lambda x: bool(set(x) & set(nation)))
    
    if season_start and season_end is None:
        mask &= df_player['season_id'] >= season_start
    
    if season_start and season_end:
        mask &= df_player['season_id'].between(season_start, season_end)
    
    if season_start is None and season_end:
        mask &= df_player['season_id'] <= season_end

    return df_player[mask].drop_duplicates(subset=['id']).reset_index(drop=True)


def select_competition_nations(competition_id):
    df_player = pd.read_csv('data/tm_players.csv')
    df_player['nationality'] = df_player['nationality'].apply(ast.literal_eval)
    df_player = df_player.to_dict('records')
    df_club = pd.read_csv('data/tm_clubs.csv').to_dict('records')

    club_ids = {club['club_id'] for club in df_club if club['id'] == competition_id}

    players = {
        player['id']: player for player in df_player if player['club_id'] in club_ids
    }

    nations = set()
    for player in players.values():
        for nation in player['nationality']:
            nations.add(nation)

    return nations


def select_competition_players(competition_id, season_start=None, season_end=None, nation=[]):
    df_player = pd.read_csv('data/tm_players.csv')
    df_player['nationality'] = df_player['nationality'].apply(ast.literal_eval)

    df_club = pd.read_csv('data/tm_clubs.csv')
    df_club = df_club[df_club['id'] == competition_id]

    df_player = pd.merge(df_player, df_club, on='club_id', how='inner', suffixes=("", "_y"))
    mask = df_player['nationality'].apply(lambda x: bool(set(x) & set(nation)))
    
    if season_start and season_end is None:
        mask &= df_player['season_id'] >= season_start
    
    if season_start and season_end:
        mask &= df_player['season_id'].between(season_start, season_end)
    
    if season_start is None and season_end:
        mask &= df_player['season_id'] <= season_end

    return df_player[mask].drop_duplicates(subset=['id']).reset_index(drop=True)


def read_sql_query(df, table=None, stmt=None):
    # type: (pd.DataFrame, str, str) -> None

    conn = sqlite3.connect(':memory:')

    try:
        df.to_sql(table, conn, index=False, if_exists='replace')
        query = stmt
        df_query = pd.read_sql_query(query, conn)
    
        return df_query
    finally:
        conn.close()


def get_int_param(value, alt=None):
    try:
        value = int(value)
    except ValueError:
        value = alt
    
    return value