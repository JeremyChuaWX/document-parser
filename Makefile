include .env
export

.PHONY: setup
setup:
	mkdir ${ARTIFACTS_PATH} ${OUTPUTS_PATH}

.PHONY: migrate
migrate:
	docker compose --profile migrate up --build -d
	docker compose wait sql_db.migrate vector_db.migrate
	docker compose --profile migrate down --remove-orphans --volumes
	docker image prune -f

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
