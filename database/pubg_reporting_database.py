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

    def insert_players(self, players):
        """
        Drop all the players into the players table.
        """

        cursor = self.connect()

        for player in players['data']:
            cursor.execute('insert into players\
                            values (\
                                %s,\
                                %s,\
                                %s);', (
                                    player['id'],
                                    player['attributes']['name'],
                                    player['attributes']['shardId']
                                    ))

        self.disconnect()

        return None

    def insert_matches(self, matches, cursor):
        """
        Because of the way the API is structured, this actually inserts data
        to both the matches and player_matches tables. Matches first otherwise
        the foreign keys will get upset, and we wouldn't want that now would
        we?
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
                    m['data']['attributes']['createdAt'][:-2],
                    m['data']['attributes']['duration'],
                    m['data']['attributes']['gameMode'],
                    m['data']['attributes']['mapName'],
                    m['data']['attributes']['isCustomMatch'],
                    m['data']['attributes']['seasonState'],
                    m['data']['attributes']['shardId']
                    )
                )



                    cursor.execute('insert into player_matches (player_id, match_id)\
                    values (\
                    %s,\
                    %s);', (player['id'], match['id'])
                    )

        self.disconnect()

        return None
