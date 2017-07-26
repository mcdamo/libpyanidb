libpyanidb
==========

Libpyanidb is a python client for the [AniDB UDP API](https://wiki.anidb.net/w/API)
Originally created by [alexer](http://alexer.net/~alexer/libpyanidb/)

This uses a local database to cache all API results, MySQL is preferred
and support for sqlite has been added.

You will require an [AniDB](https://anidb.net) account to use the API

## CLI

A basic commandline interface is included that will can query (and cache) Anime info only.

* Use included database_schema.sql to create a MySQL database for caching
* Copy dotlibpyanidb.sample as ~/.libpyanidb or /etc/libpyanidb.conf
* Update config with your AniDB account and MySQL database credentials
* Run: python cli/anidbcli.py --help
