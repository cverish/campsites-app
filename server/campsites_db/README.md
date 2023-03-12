# Campsites Database
## Table of Contents  
[Overview](#overview)  
[Tables](#tables) 
[Migrations](#migrations)

## Overview
This directory contains the code for the `campsites` database using `sqlalchemy`.

The database is a `postgresql` db which uses `alembic` for migrations.

Also contains a directory, `data`, which stores the raw data from [USCampgrounds.info](http://www.uscampgrounds.info/). See the `README` in this directory for a deeper explanation of the raw data.

## Tables
This database currently contains one table: `campsites`. View `models.py` to see the columns.

## Migrations
To create a database migration using Alembic, build the `docker-compose` file in the root directory and start the service:

`make build && make start`

Exec into the container:
`make bash`

Ensure that the `alembic` migration is up-to-date:

`make db-current` to check status of migrations

`make db-upgrade` to apply all migrations

To autogenerate an alembic migration, use

`make db-migration MESSAGE="your migration message"`

You may need to manually edit the alembic migration script, especially if you are adding enums.

To apply your alembic migration:

`make db-upgrade`

It's always a good idea to test your downgrade script at this point:

`make db-downgrade`
