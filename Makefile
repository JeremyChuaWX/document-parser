include .env
export

.PHONY: setup
setup:
	echo "creating artifacts and outputs directories ..."
	mkdir artifacts outputs
	echo "initialising example .env file ..."
	cp .env.example .env

.PHONY: migrate
migrate:
	docker compose --profile migrate up --build

.PHONY: ollama
ollama:
	ollama serve

.PHONY: start
start:
	docker compose --profile app up --build

.PHONY: stop
stop:
	docker compose --profile migrate --profile app down --remove-orphans --volumes
	docker image prune -f

.PHONY: clean
clean:
	rm -rf ${SQL_DB_DATA_PATH} ${VECTOR_DB_DATA_PATH}
