env:
	touch .env

requirements:
	pip install -r requirements.txt

requirements-test:
	pip install -r requirements_test.txt

build: env
	docker build . -t campsites-api

black:
	black .

isort:
	isort .

flake8:
	flake8

lint: flake8 isort black

db-current:
	alembic current

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-migration:
	alembic revision --autogenerate -m "$(MESSAGE)"
