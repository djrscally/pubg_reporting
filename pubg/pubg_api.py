"""
Class to manage the connections to the PUBG API
"""

import requests
import json
import time
import os
import multiprocessing
import logging

# Need a global list for multiprocessing to work properly.
matches = []

class pubg_api:

    def __init__(self, config):
        self.headers = {
            'Authorization': os.environ.get('PUBG_API_KEY'),
            'Accept': 'application/vnd.api+json'
        }

        self.base_url = 'https://api.pubg.com/shards/'

        self.shard = config['shard']
        self.player_names = config['players']
        self.matches = []
        self.player_season_stats = []
        self.player_ranked_season_stats = []
        self.player_lifetime_stats = []
        self.players = []

        # holders for response variables, for rate-limit avoidance purposes
        self.response_status_code = None
        self.response_headers = None

        return None

    def invoke_rest_api(self, url, headers, params=None):
        """
        All the calls to the API are done through this function, so that any necessary changes can easily
        be made in one place
        """

        # rate limiting goes here. Check the latest response header dict and
        # see if it has the rate limit headers. If it does and we're out of 
        # calls, wait till the reset. Otherwise, just run the func.

        # if we've actually run something already
        if self.response_status_code is not None:
            # and it has a rate limit
            if 'X-Ratelimit-Remaining' in self.response_headers.keys():
                # if the rate limit is 0
                if self.response_headers['X-Ratelimit-Remaining'] == '0':
                    # rather than a bare sleep we'll while away the time till current > reset time, so that in the case
                    # we end up waiting past the reset time of the last call due to db writes or whatever we're not unecessarily 
                    # hanging around.
                    reset_time = float(self.response_headers['X-Ratelimit-Reset'])

                    # log here since this is the first place we're _actually_ waiting
                    logging.debug('Waiting {0}s to avoid rate limiter'.format((reset_time-time.time()) + 5.))

                    while time.time() < (reset_time + 5):
                        continue

        # our waiting is done, on with the call, yo!
        r = requests.get(
            url=url,
            headers=headers,
            params=params
        )

        # store the latest response code and headers
        self.response_status_code = r.status_code
        self.response_headers = r.headers

        return r

    def get_players(self):

        module = '/players'

        i = 0

        while i < len(self.player_names):

            payload = {'filter[playerNames]': ','.join(self.player_names[i:i+10])
            }

            logging.debug("get_players:Payload = [{0}]".format(','.join(self.player_names[i:i+10])))

            try:
                r = self.invoke_rest_api(
                    url=self.base_url + self.shard + module,
                    headers=self.headers,
                    params=payload
                    )
            except Exception as e:
                logging.exception("get_players: API Request")

            try:
                self.players = self.players + r.json()['data']
            except Exception as e:
                logging.exception("get_players: Append to players")

            i += 10

        return True


    def get_matches(self, process_matches):

        with multiprocessing.Pool() as pool:
            multiprocessed_matches = pool.map(self.get_match, process_matches)

        self.matches = [i for j in multiprocessed_matches for i in j]
        logging.info("get_matches: Num Matches fetched = {0}".format(len(self.matches)))

        return True

    def get_match(self, match_id):
        """
        Fetch a single match by calling the PUBG API, and append it to the list
        of matches
        """

        matches = []

        logging.debug("get_match: match_id={0}".format(match_id))

        module = '/matches/{0}'.format(match_id)

        try:
            r = self.invoke_rest_api(
                url=self.base_url + self.shard + module,
                headers=self.headers
            )
        except Exception as e:
            logging.exception("get_match: API Request:")

        try:
            matches.append(r.json())
        except:
            logging.exception("get_match: Append to matches")

        return matches

    def get_seasons(self):
        """
        Fetch the list of seasons from the API. This shouldn't change more than
        once a month and the API documentation specifically says not to call the
        endpoint more regularly than that, so we'll cache it in the DB unless
        the time-last-called is more than 1 month ago.
        """

        module = '/seasons'

        r = self.invoke_rest_api(
            url=self.base_url + self.shard + module,
            headers=self.headers
        )
        try:
            self.seasons = r.json()['data']
        except:
            logging.exception('get_seasons: Append data to seasons')

        return None

    def get_current_season(self):
        """
        Returns the current season only from the cached list of seasons
        """

        return [season for season in self.seasons if season['attributes']['isCurrentSeason']]

    def get_player_ranked_season_stats(self, combo):
        """
        Fetches the ranked player season stats. Combo is a tuple consisting of
        (player_id, season_id).
        """

        module = '/players/{0}/seasons/{1}/ranked'.format(
            combo[0],
            combo[1]
        )

        r = self.invoke_rest_api(
            url=self.base_url + self.shard.split('-')[0] + module,
            headers=self.headers
        )

        logging.debug("get_player_ranked_season_stats: {0}: {1}: {2}".format(combo[0], combo[1], json.dumps(r.json(), indent=4)))

        if r.status_code == 200:
            try:
                self.player_ranked_season_stats.append(
                    r.json()['data']
                )
            except:
                logging.exception("get_player_ranked_season_stats: Error appending data to list")
        else:
            logging.debug("get_player_ranked_season_stats returned something other than HTTP 200")

        return None

    def get_player_season_stats(self, combo):
        """
        This call has to be rate limited, as it's pretty fast to complete which
        means it often hits the API's transaction limit and returns a html 429
        code. 4 second pauses between calls seems to avoid the issue, but I'll
        include a condition to pause for 20 seconds if it hits the issue.

        combo is a (player_id, season_id) tuple
        """

        module ='/players/{0}/seasons/{1}'.format(
            combo[0],
            combo[1]
        )

        r = self.invoke_rest_api(
            url=self.base_url + self.shard + module,
            headers=self.headers
        )

        while r.status_code == 429:
            time.sleep(10)

            r = self.invoke_rest_api(
                url=self.base_url + self.shard + module,
                headers=self.headers
            )

        logging.debug("get_player_season_stats: {0}: {1}: {2}".format(combo[0], combo[1], json.dumps(r.json(), indent=4)))

        if r.status_code == 200:
            try:
                self.player_season_stats.append(
                    r.json()['data']
                )
            except:
                logging.exception("get_player_season_stats: Error appending data to list")
        else:
            logging.debug("get_player_season_stats returned something other than HTTP 200")

        return None

    def get_player_lifetime_stats(self, process_players):

        for player in process_players:
            module = '/players/{0}/seasons/lifetime'.format(
                player
            )

            r = self.invoke_rest_api(
                url=self.base_url + self.shard + module,
                headers=self.headers
            )

            while r.status_code == 429:
                time.sleep(10)

                r = self.invoke_rest_api(
                    url=self.base_url + self.shard + module,
                    headers=self.headers
                )

            if r.status_code == 200:
                try:
                    self.player_lifetime_stats.append(
                        r.json()['data']
                    )
                except:
                    logging.exception("get_player_lifetime_stats: Error appending data to list")
            else:
                logging.debug("get_player_lifetime_stats returned something other than HTTP 200")


        return None
