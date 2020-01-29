"""
Class to manage the connections to the PUBG API
"""

import requests
import json
import time
import os

class pubg_api:

    def __init__(self, config):
        self.headers = {
            'Authorization': os.environ.get('PUBG_API_KEY'),
            'Accept': 'application/vnd.api+json'
        }

        self.base_url = 'https://api.pubg.com/shards/'

        self.player_names = config['players']
        self.matches = []
        self.player_season_stats = []
        self.player_lifetime_stats = []
        self.players = []

        return None


    def get_players(self):

        shard = 'xbox-eu'
        module = '/players'

        i = 0

        while i < len(self.player_names):

            payload = {'filter[playerNames]': ','.join(self.player_names[i:i+10])
            }

            r = requests.get(
                self.base_url + shard + module,
                headers=self.headers,
                params=payload
                )

            self.players = self.players + r.json()['data']

            i += 10

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

        shard = 'xbox-eu'
        module = '/matches/{0}'.format(match_id)

        r = requests.get(
            self.base_url + shard + module,
            headers=self.headers
        )

        return r.json()

    def get_seasons(self):
        """
        Fetch the list of seasons from the API. This shouldn't change more than
        once a month and the API documentation specifically says not to call the
        endpoint more regularly than that, so we'll cache it in the DB unless
        the time-last-called is more than 1 month ago.
        """

        shard = 'xbox-eu'
        module = '/seasons'

        r = requests.get(
            self.base_url + shard + module,
            headers=self.headers
        )
        self.seasons = r.json()['data']

        return None

    def get_player_season_stats(self):
        """
        This call has to be rate limited, as it's pretty fast to complete which
        means it often hits the API's transaction limit and returns a html 429
        code. 4 second pauses between calls seems to avoid the issue, but I'll
        include a condition to pause for 20 seconds if it hits the issue.
        """

        shard = 'xbox-eu'

        for player in self.players:
            for season in self.seasons:
                module ='/players/{0}/seasons/{1}'.format(
                    player['id'],
                    season['id']
                )

                r = requests.get(
                    self.base_url + shard + module,
                    headers=self.headers
                )

                while r.status_code == 429:
                    time.sleep(20)

                    r = requests.get(
                        self.base_url + shard + module,
                        headers=self.headers
                    )

                self.player_season_stats.append(
                    r.json()['data']
                )

                time.sleep(5)

        return None

    def get_player_lifetime_stats(self):

        shard = 'xbox-eu'

        for player in self.players:
            module = '/players/{0}/seasons/lifetime'.format(
                player['id']
            )

            r = requests.get(
                self.base_url + shard + module,
                headers=self.headers
            )

#            print(module)
#            print(player['id'])
#               print(r.text)

            self.player_lifetime_stats.append(
                r.json()['data']
            )

        return None
