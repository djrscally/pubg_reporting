#!/bin/bash

# This script installs the pubg_reporting database, along with associated
# infrastructure like the config.json file defining the parameters, the
# python files to fetch data from the API and the cron jobs to update the
# data.


MYSQL_BIN=/usr/bin/mysqlx # Remove the x for production
CONFIG_FILE=./config.jsonx # Remove the x for production

function buildconfig {

	# First we'll collect the info we need to generate the config

	read -p "Enter the Database host: " dbhost_var
	read -p "Enter the Database user: " dbuser_var
	read -sp "Enter the Database password: " dbpass_var
	read -p "Enter the PUBG shard you play in: " shard_var
	read -p "Paste in your PUBG API key: " api_var

	players=()

	# Players is a little complex as there could be any number. We'll do a simple
	# while loop to check if the person running the script is done adding their
	# players or whether to continue.

	players+=(`read -p "Enter the first player's name: "`)

	read -p "Are there any more players to add? (y/n): " exit_loop

	while [ "$exit_loop" == "y" ];
		do
			players+=(`read -p "Enter the next player's name: "`)
			read -p "Are there any more player's to add? (y/n): " exit_loop
		done

	# So we create the config file and change the permissions to 700, since there's some
	# sensitive information in here.

	touch $CONFIG_FILE
	chmod 700 $CONFIG_FILE

	# Now we drop in all the values we collected to create a json files
	echo $players
	jq -n --argjson v $players '{"players": [$v]}' > $CONFIG_FILE

	return 0
}

# Step 1. Check if all the binaries we need to exist actually do exist. If not,
# list the missing requirements and demand they go install them.



# Step 2. Check if config.json exists and build it if not.
if [ ! -r "$CONFIG_FILE" ]; then
	read -p "No config file available. Would you like to create one now? (y/n)" create_var
	if [ "$create_var" == "y" ]; then
		buildconfig
	else
		echo "This installation requires a config file. Please re-run the script later"
		exit 1
	fi
else
	echo "Confile file detected."
fi


if [ ! -x "$MYSQL_BIN" ]; then
	echo "ERROR: MySQL is missing or not in the usual place. Please either \
install it or edit this script to provide the appropriate path to the \
MYSQL_BIN variable"
else
	echo "MySQL Present and OK."
fi
