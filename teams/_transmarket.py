import json
import os
import urllib.parse

import requests
import pandas as pd


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
        try:
            data = pd.read_csv(file_name)
            data = data[data["club_id"] == club_id & data["season_id"] == season_id]
        except FileNotFoundError:
            print(f"File {file_name} not found. Fetching data from API.")
            data = self.fetch_players(club_id, season_id)
            # data = pd.read_json(data['players'])
            data = pd.DataFrame(data['players'])
            data['club_id'] = club_id
            data['season_id'] = season_id
            if save_to_file:
                data.to_csv(file_name, mode='a', index=False, header=not file_exists)
                print(f"Data saved to {file_name}")
        
        return data

    def fetch_competition_clubs(self, competition_id, season_id=None, save_to_file=False):
        """
        Get the clubs for a given competition and season.
        If the data is already cached in a file, it will be loaded from there.
        Otherwise, it will be fetched from the API. Optionally data can 
        be saved to a file.
        """
        url = self.build_competition_clubs_url(competition_id, season_id)
        file_name = (
            urllib.parse.quote(url, safe="").replace("/", "_") + ".json"
        )
        file_name = f"data/{file_name}"
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File {file_name} not found. Fetching data from API.")
            data = self.fetch_competition_clubs_data(competition_id, season_id)
            if save_to_file:
                with open(file_name, "w") as file:
                    json.dump(data, file, indent=4)

        return data
    
    def fetch_players_async(self, club_id, save_to_file=False):
        import concurrent.futures as cf

        params = [(club_id, i, save_to_file) for i in range(1990, 2026)]
        results = []

        with cf.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self.fetch_players, *param): param for param in params}
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
        url = self.build_players_url(club_id, season_id)
        file_name = (
            urllib.parse.quote(url, safe="").replace("/", "_") + ".json"
        )
        file_name = f"data/{file_name}"
        try:
            os.remove(file_name)
            print(f"File {file_name} deleted.")
        except FileNotFoundError:
            print(f"File {file_name} not found.")