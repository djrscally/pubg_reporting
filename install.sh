#!/bin/bash

# This script installs the pubg_reporting database, along with associated
# infrastructure like the config.json file defining the parameters, the
# python files to fetch data from the API and the cron jobs to update the
# data.


MYSQL_BIN=/usr/bin/mysql
PYTHON_BIN=/usr/bin/python3
CONFIG_FILE=./config.json
JQ_BIN=/usr/bin/jq

# First a helper function to check that the config file actually exists!
checkconfig(){
	if [ ! -r "$CONFIG_FILE" ]; then
		read -p "No config file found. Would you like to create one now? (y/n) " create_var
		if [ "$create_var" == "y" ]; then
			$PYTHON_BIN ./config.py
		else
			echo "This installation requires a config file. Please re-run the script later"
			exit 1
		fi
	else
		echo "Confile file detected."
	fi
}

# Install routine First

install() {

	# Step 1. Check if the programs we need are actually installed, and if not
	# send them to fix that.

	if [ ! -x "$MYSQL_BIN" ]; then
		echo "ERROR: MySQL is not installed or not in the usual place. Please either \
 install it or edit this script to provide the appropriate path to the \
 MYSQL_BIN variable"
		exit 1
	fi

	if [ ! -x "$PYTHON_BIN" ]; then
		echo "ERROR: Python3 is not installed or not in the usual place. Please either\
install it or edit this script to provide the appropriate path to the PYTHON_BIN\
variable"
		exit 1
	fi

	if [ ! "$JQ_BIN" ]; then
		echo "ERROR: jq is not installed. jq is a terminal tool for parsing JSON, please\
 install it and re-run install.sh"
 		exit 1
	fi

	echo "All dependencies met..."

	# Step 2. Check if config.json exists and build it if not.

	checkconfig

	# Load the database login
	DB_UN=`jq ".db_un" config.json`
	DB_PW=`jq ".db_pw" config.json`

	# run the create_db.sql script to create the database
	$MYSQL_BIN -u "$DB_UN" -p "$DB_PW" < database/create_db.sql
	# run the sync.py script to fill it with data
	$PYTHON_BIN ./sync.py
	# create a cron job to automate the script to run every night.

}


case "$1" in
	install)
		install
	;;
	uninstall)
		echo "UNINSTALL!!"
	;;
	reload)
		echo "RELOAD!!"
	;;
	*)
		echo "Usage: $0 {install|uninstall|reload}"
esac
echo "$1 operation complete."
