# PUBG Reporting

### Database structure and sync scripts to build a reporting database fetching data from the PUBG API. This will allow you to use tools like Metabase to build custom dashboards for your team. Make pretty graphs, win nerd cred.

### Status:

Everything should be basically useable. Installation is relatively simple. I want to flesh this readme out with some documentation about the tables and available views, as well as create some more useful views to begin with, but go ahead and use it now if you want to get started.

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
    PUBGDB_CONFIG_PATH  - holding a path to the config.json (NOT including the file name, so for example C:\Users\dscally\Documents\dev\pubg_reporting\) defining which players you want to sync, in this format:

```
{

  "players":[
    "Player1",
    "Player2",
    ...,
  ]
}
```

  6. Run these commands to get the files and move into the repo's directory, then build the database structure:

```  
$ git clone https://github.com/djrscally/pubg_reporting
$ cd pubg_reporting
$ python3 -m venv venv
$ source ./venv/bin/activate
$ (venv) pip3 install -r requirements.txt
$ (venv) python sync.py --build-only
```

The script wil build the database for you. At this point all the infrastructure is set up; you can run `python sync.py` to pull in data for the players you defined in the config.json file. 

Once the script completes, you should be good to go; you can hook in whichever analysis tool takes your fancy. I like [Metabase](https://www.metabase.com/).

#### Automating things.

Obviously you can run the sync manually, but that's annoying. To automate things I recommend a cron job. As a precursor step, you'll need to create a file that sets the environment variables you've manually set above; these will need to be made available to the process before it's called, otherwise it won't know how to login to MySQL. To do that, do something like the following:

```
mkdir ~/.secrets
touch ~/.secrets/pubg
chmod 700 ~/.secrets
```

This creates a directory called .secrets in your home folder to which only you have access, and additionally creates a file called pubg - use whatever text editor you prefer to fill that file with the 
 Run `crontab -e` and simply create an entry to periodically run the sync, for example:

`0 0,8,16 /home/user/pubg_reporting/sync.sh`

Would run the sync 3 times per day, at midnight, 8 am and 4pm.






#### For Windows

**Please Note:** I have not tested this at all. It ought to work fine, but no promises.
At **some point** I'll get round to making a PowerShell script to replicate install.sh, but for now...

1. Follow the same mandatory pre-requisite steps as for Linux, but skip \#3.
2. If you can `git clone https://github.com/djrscally/pubg_reporting` in PowerShell then do that. If not, just go to that repo in a browser and hit the green "Clone or Download" button
and download a .zip - unzip that somewhere appropriate and move into it
3. Create a file called config.json Use whatever text editor you prefer to populate the config file in the following format:



Because that file has the connection info saved to it, you'll want to change the permissions so that yours is the only user allowed to read it. Right click the file and go to Properties > Security, then click Advanced. _untick_ "Include inheritable permissions..." and then use the Change Permissions button to deny Read access to everyone but you (or some other users as appropriate, your call).

4. Run databases/create_db.sql on your MySQL instance
5. Open PowerShell in the pubg_reporting directory and run `py -3 ./sync.py`

And that should work fine. Use Task Scheduler to run C:\\path\\to\\python\\py.exe with the argument C:\\path\\to\\repo\\pubg_reporting\\sync.py and the data should update on the schedule you specify

