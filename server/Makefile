env:
	touch .env

compile-requirements:
	pip-compile -U requirements.in -o requirements.txt
	pip-compile -U requirements_test.in -o requirements_test.txt

requirements:
	pip install -r requirements.txt

requirements-test: requirements
	pip install -r requirements_test.txt

build: env
	docker build . -t campsites-api

lint:
	ruff format && ruff check

db-current:
	alembic current

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-migration:
	alembic revision --autogenerate -m "$(MESSAGE)"
