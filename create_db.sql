-- -------------------------------------------------------------------
-- This script builds a reporting database to hold data fetched from
-- the pubg API, which can then be used with data analysis tools to
-- make pretty graphs and win nerd/gamer cred.
--
-- Author: djrscally
--
-- Change Log:
-- 08/11/2018: Initial build, tables made.
-- -------------------------------------------------------------------

-- start by reinitialising the db if it exists already
drop database if exists pubg_reporting;
create database if not exists pubg_reporting;

use pubg_reporting;

-- players table, which is fairly minimal
create table players (
	player_id nvarchar(255) not null primary key
    , player_name nvarchar(255) not null
    , shard_id nvarchar(255)
);

-- seasons table, also minimal
create table seasons (
	season_id nvarchar(255) not null primary key
    , is_current_season bool not null
    , is_off_season bool not null
);

-- matches table, details about the actual rounds played (although
-- not any stats which is weird)

create table matches (
	match_id nvarchar(255) not null primary key
    , createdAt datetime not null
    , duration int not null
    , gameMode nvarchar(255) not null
    , mapName nvarchar(255) not null
    , isCustomMatch bool not null
    , seasonState nvarchar(255) not null
    , shardId nvarchar(255) not null
);

-- relational table tying players to the matches they have been
-- in, but again no stats.

create table player_matches (
	player_match_id int not null primary key auto_increment
    , player_id nvarchar(255) not null
    , match_id nvarchar(255) not null
    , foreign key (player_id) references players(player_id) on update cascade on delete cascade
    , foreign key (match_id) references matches(match_id) on update cascade on delete cascade
);

-- relational table tying matches to the season that they're in

create table season_matches (
	season_match_id int not null primary key auto_increment
    , season_id nvarchar(255) not null
    , match_id nvarchar(255) not null
    , foreign key (season_id) references seasons(season_id) on update cascade on delete cascade
    , foreign key (match_id) references matches(match_id) on update cascade on delete cascade
);

-- a players stats for a season

create table player_season_stats (
	season_stats_id int not null primary key auto_increment
    , season_id nvarchar(255) not null
    , game_mode nvarchar(255) not null
    , assists int not null
    , bestRankPoint int not null
    , boosts int not null
    , dBNOs int not null
    , dailyKills int not null
    , damageDealt int not null
    , days int not null
    , dailyWins int not null
    , headshotKills int not null
    , heals int not null
    , killPoints int not null
    , kills int not null
    , longestKill int not null
    , longestTimeSurvived int not null
    , losses int not null
    , maxKillStreaks int not null
    , mostSurvivalTime int not null
    , rankPoints int not null
    , revives int not null
    , rideDistance int not null
    , roadKills int not null
    , roundMostKills int not null
    , roundsPlayed int not null
    , suicides int not null
    , swimDistance int not null
    , teamKills int not null
    , timeSurvived int not null
    , top10s int not null
    , vehicleDestroys int not null
    , walkDistance int not null
    , weaponsAcquired int not null
    , weeklyKills int not null
    , weeklyWins int not null
    , winPoints int not null
    , wins int not null
    , foreign key (season_id) references seasons(season_id) on update cascade on delete cascade
);

-- a players stats in all seasons combined.

create table player_lifetime_stats (
	lifetime_stats_id int not null primary key auto_increment
    , player_id nvarchar(255) not null
    , assists int not null
    , bestRankPoint int not null
    , boosts int not null
    , dBNOs int not null
    , dailyKills int not null
    , damageDealt int not null
    , days int not null
    , dailyWins int not null
    , headshotKills int not null
    , heals int not null
    , killPoints int not null
    , kills int not null
    , longestKill int not null
    , longestTimeSurvived int not null
    , losses int not null
    , maxKillStreaks int not null
    , mostSurvivalTime int not null
    , rankPoints int not null
    , revives int not null
    , rideDistance int not null
    , roadKills int not null
    , roundMostKills int not null
    , roundsPlayed int not null
    , suicides int not null
    , swimDistance int not null
    , teamKills int not null
    , timeSurvived int not null
    , top10s int not null
    , vehicleDestroys int not null
    , walkDistance int not null
    , weaponsAcquired int not null
    , weeklyKills int not null
    , weeklyWins int not null
    , winPoints int not null
    , wins int not null
    , foreign key (player_id) references players(player_id) on update cascade on delete cascade
);
