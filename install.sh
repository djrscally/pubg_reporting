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
			# chmod 700 to deny read permissions to other users, since the file contains
			# db credentials.
			chmod 700 $CONFIG_FILE
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

	# Step 3. Run the create_db.sql script to create the database
	echo "Please enter the password for the MySQL user (to avoid it appearing in history)."
	{
	eval "$MYSQL_BIN -u $DB_UN -p < database/create_db.sql"
	} || {
	echo "ERROR: There was a problem initialising the database. Exiting"
	exit 1
	}
	# Step 4. Run the sync.py script to fill it with data
	{
	$PYTHON_BIN ./sync.py
	} || {
	echo "ERROR: There was a problem running sync.py. Exiting"
	exit 1
	}

	# Step 5. Create a cron job to automate the script to run every night at 4am
	crontab -l >> mycron
	echo "0 4 * * * $PYTHON_BIN $PWD/sync.py" >> mycron
	crontab mycron
	rm mycron

}

uninstall(){

	# Load the DB Credentials

	DB_UN=`jq ".db_un" config.json`
	DB_PW=`jq ".db_pw" config.json`

	# Step 1. Remove the cron job
	crontab -l | grep -v "$PYTHON_BIN $PWD/sync.py" | crontab -

	# Step 2. Nuke the database
	echo "Please enter the password for the MySQL user (to avoid it appearing in history)"
	{
	eval "$MYSQL_BIN -u $DB_UN -p < database/delete_db.sql"
	} || {
	echo "ERROR: There was a problem deleting the database. Exiting"
	exit 1
	}
	# And that's it. We'll leave the files, rm still works if they want to get rid
	# of the dir entirely.
	echo "Uninstall complete."
}



case "$1" in
	install)
		install
	;;
	uninstall)
		uninstall
	;;
	*)
		echo "Usage: $0 {install|uninstall}"
esac
