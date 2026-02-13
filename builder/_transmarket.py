import concurrent.futures as cf
import json
import os
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

    def get_players(self, club_id, season_id, save_to_file=False):
        file_name = f"data/tm_players.csv"
        file_exists = os.path.exists(file_name)
        data = None
        w = True
        df = None
        if file_exists:
            df = pd.read_csv(file_name)
            data = df[(df["club_id"] == club_id) & (df["season_id"] == season_id)]
            w = False if not data.empty else True
        if data is None or data.empty:
            print(f"Data is empty. Fetching data from API.")
            data = self.fetch_players(club_id, season_id)
            data = pd.DataFrame(data['players'])
            data['club_id'] = club_id
            data['season_id'] = season_id
        if save_to_file and w:
            # data.to_csv(file_name, mode='a', index=False, header=not file_exists)
            if df is not None:
                df_final = pd.concat([df, data], ignore_index=True, sort=False)
            else:
                df_final = data
            df_final.to_csv(file_name, index=False)
            print(f"Data saved to {file_name}")
        
        return data

    def get_competition_clubs(self, competition_id, season_id=None, save_to_file=False):
        data = self.fetch_competition_clubs(competition_id, season_id)
        data = pd.DataFrame(data)

        return data
    
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