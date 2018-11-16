# PUBG Reporting

### Database structure and sync scripts to build a reporting database fetching data from the PUBG API. This will allow you to use tools like Metabase to build custom dashboards for your team. Make pretty graphs, win nerd cred.

### Status:

Definitely whatever pre-pre-Alpha is called, but the scripts will set up the db
and fetch the data from the API now, so it's basically useable if not especially
user friendly just yet.

#### Installation:

As install.sh isn't working properly yet you'd have to do this pretty manually.
Pre-requisite steps:

  1. Make sure Python3 is installed.
  2. Make sure MySQL is installed
  3. Make sure Python libraries [requests](http://docs.python-requests.org/en/master/) and the [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html) are installed
  4. Create a MySQL user with `create database ...;` privileges

Start by running these commands to get the files and move into this directory,
then create a config.json file

```  
$ git clone https://github.com/djrscally/pubg_reporting
$ cd pubg_reporting
$ touch config.json
```

Use whatever text editor you prefer to populate the config file in the following
format:

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

Because that file has the connection info saved to it, you'll want to change the
permissions so that yours is the only user allowed to read it:

`$ chmod 700 config.json`

From here, it should just be a case of running the db creation and data population
scripts

```
$ mysql -u << mysql user >> -p < database/create_db.sql
$ python3 ./sync.py
```

And you should be up and running!
