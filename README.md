# Campsites App

## Background
A full-stack application for exploring public campsites across the US and Canada.

The app currently contains a filterable list view of all campsites with server-side filtering, sorting, and pagination. It's also mobile-friendly! More features to come, go to the [Project Status](#project-status) section for more details.

View the work-in-progress application [here](https://campsites.veri.sh).

## Table of Contents
- [Background](#background)
- [Technologies](#technologies)
- [Setup](#setup)
- [Running the Application](#running-the-application)
	- [Server](#server)
	- [Client](#client)
- [Development](#development)
- [Project Status](#project-status)
- [Credits](#credits)

## Technologies
Server: `python`
- Postgres database (with `sqlalchemy` ORM)
- API using `FastApi`
- Docker

Front-end:
- React with TypeScript
- [Mantine](https://mantine.dev/) component library
- `react-query` for asynchronous data management

## Setup
Installations:
- [Docker](https://www.docker.com/)
- [Node.js](https://nodejs.org/en)

Verify these installs by running
```bash
$ docker --version
$ npm --version
```

## Running the application
### Server
In the root directory, run

```bash
$ make build
$ make start
```

to build and start the backend services.

**You will need to manually run the alembic migration** (on the list to fix):

```bash
$ make bash
$ make db-upgrade
```

After doing so, you may need to restart the docker services.

The API is accessible at [`localhost:8000`](http://localhost:8000). To view the Swagger docs, visit [`localhost:8000/docs`](http://localhost:8000/docs) in your browser.

Data can be uploaded via the `/campsites/upload` endpoint; CSV data files can be found in `/campsites_db/data`. The data in these CSVs has been very mildly cleaned from the source data, so I recommend you use these files.

### Client
Within the `/client` folder, run
```bash
$ make init
```
This will copy the contents of `.env.template` into `.env.local` and install the `node_modules`. You'll need to change the values in `.env.local` to be specific to your setup -- local development values are specified in the template.

To run the application locally:
```bash
$ npm start
```

Once it is running, visit [`localhost:3000`](http://localhost:3000) in your browser to view the application.

## Development
Once the docker container is running, changes to files in `/server` will be synced automatically -- no need to rebuild during development. However, you will need to `docker exec` into the docker container (via `make bash`) to apply alembic migrations.

To interact directly with the postgresql database, ensure you have, at a minimum, `psql` installed:

```bash
$ psql --version
```

If you do not, you can install it via [the installer](https://www.postgresql.org/download/) or manually via [`brew`](https://brew.sh/):

```bash
$ brew install postgresql
```

(or for the minimal version, `libpq`, but this requires more setup.)

Once you have verified installation, the following command will open a postgresql terminal, after which you will be prompted for a `password`:

```bash
$ psql -h 127.0.0.1 -p 5555 -d {database} -U {user}
```

In local development, `database`, `user`, and `password` are all `postgres`.

You can use
```bash
$ make psql-terminal
```
as a shortcut in local development; you will still be prompted for a password.

## Testing
I've begun work on adding test suites for the API within the docker container. The test suite spins up a fresh test database for the entire test suite, and each test function runs within its own session that is wiped before the next test. To run tests, ensure that the docker container is running with `make start`, then run

```bash
$ make test
```

Rather than using static fixtures for objects, I'm using model factories to generate the necessary objects for each test. Because of how the database fixtures are set up, these factories cannot be called directly; instead, the name of the factory fixture must be passed to the test function. In essence,

```python
# doesn't work
from campsites_api.tests.factories import CampsiteFactory

def my_test():
  c = CampsiteFactory.create()
```

will throw a `RuntimeError: No session provided`. One *should* be able to fix this by setting the `factory_class._meta.sqlalchemy_session` within the `db_session` but it wasn't being passed properly. Instead, the factory fixture should be used:

```python
# use this instead
def my_test(campsite_factory):
  c = campsite_factory.create()
```

## Project Status
This project is still a work-in-progress, with basic backend functionality completed and the frontend in active development.

- [ ] backend
  - [x] database containing campgrounds
  - [x] basic endpoints
  - [x] file upload
  - [x] campsite list basic filtering and sorting
  - [x] geolocation support
  - [ ] ability to create trips
- [ ] frontend
  - [x] list view
  - [x] list filtering and sorting
  - [ ] detail page
  - [ ] map view
  - [ ] trip planner
- [ ] infrastructure
  - [ ] apply alembic migration automatically in the docker container
  - [x] more functional `Makefile`'s
- [ ] Good coding practices
  - [ ] tests
  - [x] linting

## Credits
- Data gratefully pulled from [USCampgrounds](http://www.uscampgrounds.info/).
