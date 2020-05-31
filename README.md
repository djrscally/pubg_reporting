# PUBG Reporting

### Database structure and sync scripts to build a reporting database fetching data from the PUBG API. This will allow you to use tools like Metabase to build custom dashboards for your team. Make pretty graphs, win nerd cred.

### Status:

Everything should be basically useable. Installation is relatively simple. I want to flesh this readme out with some documentation about the tables and available views, as well as create some more useful views to begin with, but go ahead and use it now if you want to get started.

### Usage:

```
Usage: sync.py [OPTIONS]

  Program to sync data from the Player Unknown Battlegrounds API into a
  MySQL database, for analysis and pretty nerd graphs.

Options:
  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Level of detail to include in logs
  --echo                          Echo SQL Alchemy output to stdout
  --help                          Show this message and exit.
```

### Installation:

#### For Linux
Follow these mandatory pre-requisite steps:

  1. Make sure Python3 is installed.
  2. Make sure MySQL is installed
  3. Create a db on your MySQL server for the sync scripts to write data into.
  4. Create a MySQL user for the scripts to use. You can use an existing one obviously, but I'd suggest a dedicated user; never a bad idea to separate privileges. Once you've created the user in the mysql shell run `grant all on $(db_name).* to '$(db_user)'@'localhost';` and then `flush privileges;`. Replace $(db_name) and $(db_user) with the appropriate values that you've chosen
  5. Create the following environment variables:

    PUBG_API_KEY - holding your API key
    PUBGDB_HOST  - holding the address to your MySQL server (probably localhost)
    PUBGDB_DATABASE  - holding the name of the db you want to use on the MySQL server
    PUBGDB_USERNAME  - holding the username of the MySQL user to connect to the DB
    PUBGDB_PASSWORD  - holding the password for the above MySQL user
    PUBGDB_CONFIG_PATH  - holding a path to the config.json (NOT including the file name, so for example C:\Users\dscally\Documents\dev\pubg_reporting\) defining which players you want to sync plus your gaming shard, in this format:

```
{

  "players":[
    "Player1",
    "Player2",
    ...,
  ],
  "shard":"xbox-eu"
}
```

  6. Run these commands to get the files and move into the repo's directory, then build the database structure:

```  
$ git clone https://github.com/djrscally/pubg_reporting
$ cd pubg_reporting
$ python3 -m venv venv
$ source ./venv/bin/activate
$ (venv) pip3 install -r requirements.txt
$ (venv) alembic upgrade head
```

The script will build the database for you. At this point all the infrastructure is set up; you can run `python sync.py` to pull in data for the players you defined in the config.json file. 

Once the script completes, you should be good to go; you can hook in whichever analysis tool takes your fancy. I like [Metabase](https://www.metabase.com/).

#### Upgrading to newer versions of the code

I recommend you stick to master branch, or some weird and wonderful things are likely to happen. If you pull from master to get new code, make sure you run alembic's upgrade function in case some changes were made to the underlying database; that will handle the changes to the db for you. You should definitely take a backup first though, just in case:

```
$ mysqldump --databases your-database-name | gzip /path/to/backup/folder/your-database-name.sql.gz
$ git pull
$ source ./venv/bin/activate
$ (venv) alembic upgrade head
```

And that should bring both code and database into line with the master branch. **If you got the code before I was using alembic** then you first need to tell alembic to register the DB against the intial revision; run `alembic stamp 5d9f2ca7b98b` before attempting `alembic upgrade head` and all will be well.


#### Automating things.

Obviously you can run the sync manually, but that's annoying. To automate things I recommend a cron job. As a precursor step, you'll need to create a file that sets the environment variables you've manually set above; these will need to be made available to the process before it's called, otherwise it won't know how to login to MySQL. To do that, do something like the following:

```
mkdir ~/.secrets
touch ~/.secrets/pubg
chmod 700 ~/.secrets
```

This creates a directory called .secrets in your home folder to which only you have access, and additionally creates a file called pubg - use whatever text editor you prefer to fill that file with the commands needed to fill the environment variables, for example

```
export PUBGDB_HOST="localhost"
export PUBGDB_DATABASE="pubg"
export PUBGDB_USERNAME="pubg"
export PUBGDB_PASSWORD="pubg"
export PUBG_API_KEY="<< API Key Goes Here >>"
export PUBGDB_CONFIG_PATH="/path/to/config/file/"
```

You can then "source" that file before running `python sync.py` and it'll work fine. Run `crontab -e` and simply create an entry to periodically run the sync, for example:

`0 0,8,16 0 0 0 . /home/user/.secrets/pubg && /home/user/pubg_reporting/venv/bin/python3 /home/user/pubg_reporting/sync.py OPTIONS`

Would run the sync 3 times per day, at midnight, 8 am and 4pm. Replace `OPTIONS` with anything you want to set, like `--log-level DEBUG` to get verbose output to sync.log.


#### For Windows

Everything will work fine, but you don't have CRON obviously. Use Task Scheduler instead, and for setting the envvars have Task Scheduler run a .ps1 file in this form:

```
$env:PUBGDB_HOST="localhost"
$env:PUBGDB_DATABASE="pubg"
$env:PUBGDB_USERNAME="pubg"
$env:PUBGDB_PASSWORD="pubg"
$env:PUBG_API_KEY="<< API Key Goes Here >>"
$env:PUBGDB_CONFIG_PATH="/path/to/config/file/"
```

Otherwise, should work identically.