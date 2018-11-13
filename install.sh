#!/bin/bash

# This script installs the pubg_reporting database, along with associated
# infrastructure like the config.json file defining the parameters, the
# python files to fetch data from the API and the cron jobs to update the
# data.


MYSQL_BIN=/usr/bin/mysqlddd
CONFIG_FILE=./config.json22

# Step 1. Build config.json
if [ -r "$CONFIG_FILE" ]; then
	echo "Config file detected!"
else
	echo "No config file available. Would you like to create one now? (y/n)"
	read create_var
	if [ "$create_var" == "y" ]; then
		buildconfig
	else
		echo "This installation requires a config file. Please re-run the script later"
		exit 1
	fi
fi


if [ ! -x "$MYSQL_BIN" ]; then
	echo "ERROR: MySQL is missing or not in the usual place. Please either \
install it or edit this script to provide the appropriate path to the \
MYSQL_BIN variable"
else
	echo "MySQL Present and OK."
fi

install() {
	echo "I'm a placeholder too!"
}

buildconfig() {
	echo "I'm a placeholder too!"
}
