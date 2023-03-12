env:
	touch .env

build: env
	docker-compose build --no-cache

start:
	docker-compose up --detach --remove-orphans

stop:
	docker-compose stop

down:
	docker-compose down --remove-orphans

bash:
	docker exec -it campsites_server /bin/bash
