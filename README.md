# PUBG Reporting

### Database structure and sync scripts to build a reporting database fetching data from the PUBG API. This will allow you to use tools like Metabase to build custom dashboards for your team. Make pretty graphs, win nerd cred.

### Status:

Definitely whatever pre-pre-Alpha is called, but the scripts will set up the db
and fetch the data from the API now, so it's basically useable if not especially
user friendly just yet.

Everything should be basically useable. Installation is relatively simple

### Assumptions

That you're running this onto a server that's awake at 4am, because that's when it's
gonna schedule the cron job. If that's not true just run `install.sh` and then afterwards
edit the crontab with

`$ crontab -e`

Change `0 4 * * *` to a setting that suits you better.

Also, I assume you're using Linux. If you're on Windows then this will all still work fine, except
for the install script. See below for instructions on what to do in that case.

### Installation:

#### For Linux
Follow these mandatory pre-requisite steps:

  1. Make sure Python3 is installed.
  2. Make sure MySQL is installed
  3. Make sure [jq](https://stedolan.github.io/jq/) is installed.
  4. Make sure Python libraries [requests](http://docs.python-requests.org/en/master/) and the [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html) are installed
  5. Create a MySQL user with `create database ...;` privileges

Run these commands to get the files and move into the repo's directory, then run the install.sh script.

```  
$ git clone https://github.com/djrscally/pubg_reporting
$ cd pubg_reporting
$ ./install.sh install
```

The script will collect some information from you including the names of all the players
that you want to track, your database connection details and the PUBG shard and API key to
use. It will then build the database and populate it by fetching data from the API.

Once the script completes, you should be good to go; you can hook in whichever analysis tool
takes your fancy. I like [Metabase](https://www.metabase.com/).

#### For Windows

**Please Note:** I have not tested this at all. It ought to work fine, but no promises.
At **some point** I'll get round to making a PowerShell script to replicate install.sh, but for now...

1. Follow the same mandatory pre-requisite steps as for Linux, but skip \#3.
2. If you can `git clone https://github.com/djrscally/pubg_reporting` in PowerShell then do that. If not, just go to that repo in a browser and hit the green "Clone or Download" button
and download a .zip - unzip that somewhere appropriate and move into it
3. Create a file called config.json Use whatever text editor you prefer to populate the config file in the following format:

```
{

  "players":[
    "Player1",
    "Player2",
    ...,
  ],
  "api_key":"<< api key goes here >>",
  "db_host":"<< database host >>",
  "db_name":"<< database name >>",
  "db_un":"<< the user you created >>",
  "db_pw":"<< the password for the user >>",
  "shard":"<< the shard your team plays in >>"

}
```

Because that file has the connection info saved to it, you'll want to change the permissions so that yours is the only user allowed to read it. Right click the file and go to Properties > Security, then click Advanced. _untick_ "Include inheritable permissions..." and then use the Change Permissions button to deny Read access to everyone but you (or some other users as appropriate, your call).

4. Run databases/create_db.sql on your MySQL instance
5. Open PowerShell in the pubg_reporting directory and run `py -3 ./sync.py`

And that should work fine. Use Task Scheduler to run C:\\path\\to\\python\\py.exe with the argument C:\\path\\to\\repo\\pubg_reporting\\sync.py and the data should update on the schedule you specify

### Uninstallation

This involves removing the cron job so it doesn't try and run the daily sync anymore, and deleting the database. Just move into the repo's directory and run install.sh but tell it to uninstall instead:

```
$ cd pubg_reporting
$ ./install.sh uninstall
```

And that should be it.
