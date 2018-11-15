"""
Class to manage the connections to the PUBG API
"""

import requests
import json


class pubg_api:

    def __init__(self, config):
        self.headers = {
            'Authorization': config['api_key'],
            'Accept': 'application/vnd.api+json'
        }

        self.base_url = 'https://api.pubg.com/shards/{0}'.format(
            config['shard']
        )

        self.player_names = config['players']
        self.matches = []
        self.player_season_stats = []
        self.player_lifetime_stats = []

        return None


    def get_players(self):

        module = '/players'
        payload = {'filter[playerNames]': ','.join(self.player_names)
        }

        r = requests.get(
            self.base_url + module,
            headers=self.headers,
            params=payload
            )

        self.players = r.json()['data']

        return True


    def get_matches(self):

        processed_matches = []

        for player in self.players:
            for match in player['relationships']['matches']['data']:
                if match['id'] in processed_matches:
                    continue
                else:
                    processed_matches.append(match['id'])
                    self.matches.append(self.get_match(match['id']))

        return True

    def get_match(self, match_id):
        """
        Fetch a single match by calling the PUBG API, and return the json
        """

        module = '/matches/{0}'.format(match_id)

        r = requests.get(
            self.base_url + module,
            headers=self.headers
        )

        return r.json()['data']

    def get_seasons(self):
        """
        Fetch the list of seasons from the API. This shouldn't change more than
        once a month.
        """

        module = '/seasons'

        r = requests.get(
            self.base_url + module,
            headers=self.headers
        )

        self.seasons = r.json()['data']

        return None

    def get_player_season_stats(self):

        for player in self.players:
            for season in self.seasons:
                module ='/players/{0}/seasons/{1}'.format(
                    player['id'],
                    season['id']
                )
                r = requests.get(
                    self.base_url + module,
                    headers=self.headers
                )
                self.player_season_stats.append(
                    r.json()['data']
                )

        return None

    def get_player_lifetime_stats(self):

        for player in self.players:
            module = '/players/{0}/seasons/lifetime'.format(
                player['id']
            )

            r = requests.get(
                self.base_url + module,
                headers=self.headers
            )

            self.player_lifetime_stats.append(
                r.json()['data']
            )

        return None
