"""
Class to manage the connection and transactional functions for the MySQL
database.
"""

import mysql.connector as mysql


class pubg_database:

    def __init__(self, config):
        """
        Define connection parameters for the MySQL connection, and that's
        more or less it.
        """

        self.host = config['db_host']
        self.user = config['db_un']
        self.password = config['db_pw']
        self.database = config['db_name']

        return None

    def connect(self):
        """
        Connect to the database. This is going to be transient and close after
        each transactional function is finished (or rather immediately before
        the return statement).
        """

        self.conn = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            )

        return self.conn.cursor()

    def disconnect(self):
        """
        Provide the facility to exit nicely. No sense in leaving connections
        hanging around.
        """
        self.conn.close()

        return None

    def commit(self):
        """
        Commits the transaction and nothing more
        """

        self.conn.commit()

        return None

    def insert_players(self, players):
        """
        Drop all the players into the players table.
        """

        cursor = self.connect()

        for player in players:
            cursor.execute('insert into players\
                            values (\
                                %s,\
                                %s,\
                                %s);', (
                                    player['id'],
                                    player['attributes']['name'],
                                    player['attributes']['shardId']
                                    ))
        self.commit()
        self.disconnect()

        return True

    def insert_matches(self, matches):
        """

        """

        cursor = self.connect()

        for match in matches:
            cursor.execute(
                'insert into matches\
                values (\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s,\
                %s);', (
                    match['id'],
                    match['attributes']['createdAt'][:-2],
                    match['attributes']['duration'],
                    match['attributes']['gameMode'],
                    match['attributes']['mapName'],
                    match['attributes']['isCustomMatch'],
                    match['attributes']['seasonState'],
                    match['attributes']['shardId']
                    )
                )
        self.commit()
        self.disconnect()

        return True

    def insert_player_matches(self, players):

        cursor = self.connect()

        for player in players:
            for match in player['relationships']['matches']['data']:
                cursor.execute(
                    'insert into player_matches (player_id, match_id)\
                    values (%s, %s);',
                    (player['id'], match['id'])
                )
        self.commit()
        self.disconnect()

        return True

    def insert_seasons(self, seasons):

        cursor = self.connect()

        for season in seasons:
            cursor.execute(
                'insert into seasons values (%s, %s, %s);',
                (
                    season['id'],
                    season['attributes']['isCurrentSeason'],
                    season['attributes']['isOffSeason']
                )
            )

        self.commit()
        self.disconnect()

        return True
