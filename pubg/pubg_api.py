"""
Class to manage the connections to the PUBG API
"""

import requests
import json
import time
import os
import click
import logging

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

            logging.debug("get_players:Payload = [{0}]".format(','.join(self.player_names[i:i+10])))

            try:
                r = requests.get(
                    self.base_url + shard + module,
                    headers=self.headers,
                    params=payload
                    )
            except Exception as e:
                logging.error("get_players: API Request: {0}".format(e.Message))

            try:
                self.players = self.players + r.json()['data']
            except:
                logging.error("get_players: Append to players: {0}".format(e.message))

            i += 10

        return True


    def get_matches(self):

        processed_matches = []

        with click.progressbar(self.players, label="Iterating over players") as pbar:
            for player in pbar:
                with click.progressbar(player['relationships']['matches']['data'], label="Getting matches for player") as mbar:
                    for match in mbar:
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


        /seasons/{seasonId}/gameMode/{gameMode}/players
        "https://api.pubg.com/shards/$platform/seasons/$seasonId/gameMode/$gameMode/players?filter[playerIds]=$playerId-1,$playerId-2" \

        duo
        duo-fpp
        solo
        solo-fpp
        squad
        squad-fpp



        shard = 'xbox-eu'

        game_modes = ['duo', 'duo-fpp', 'solo', 'solo-fpp', 'squad', 'squad-fpp']

        for season in self.seasons:
            for gm in game_modes:

                i = 0

                while i < len(self.players):

                module = '/seasons/{0}/gameMode/{1}/players?filter[playerIds]={2}'.format(season['id'], gm, ','.join(self.player_names[i:i+10])

                r = requests.get(
                    self.base_url + shard + module,
                    headers=self.headers
                )
        """

        shard = 'xbox-eu'

        with click.progressbar(self.players, label='Fetching Player Season Stats') as bar:
            for player in bar:
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

            while r.status_code == 429:
                time.sleep(20)

                r = requests.get(
                    self.base_url + shard + module,
                    headers=self.headers
                )

            self.player_lifetime_stats.append(
                r.json()['data']
            )

        return None
