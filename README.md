# Campsites App

** Currently a WIP, backend-only. Frontend to come ✨ **

A full-stack application for exploring public campsites across the US and Canada.

Data gratefully pulled from [USCampgrounds](http://www.uscampgrounds.info/).

## Running the application
Ensure you have [Docker](https://www.docker.com/) installed.

In the root directory, run

`make build && make start`

to build and start the backend services.

** You will need to mamually run the alembic migration ** (on the list to fix):
`make bash`
`make db-upgrade`

After doing so, you may need to restart the docker services.

The API is accessible at `localhost:8000`.

Data can be uploaded via the `/campsites/upload` endpoint; CSV data files can be found in `/campsites_db/data`. The data in these CSVs has been very mildly cleaned from the source data, so I recommend you use this.

## TODO
- [ ] apply alembic migration automatically in the docker container
- [ ] backend campsite filtering and sorting
- [ ] frontend
- [ ] tests
- [ ] linting
