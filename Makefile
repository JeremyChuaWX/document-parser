include .env
export

.PHONY: setup
setup:
	echo "creating artifacts and outputs directories..."
	@mkdir artifacts outputs
	echo "initialising example .env file..."
	@cp .env.example .env

.PHONY: vector_db
vector_db:
	echo "initialising vector DB..."

.PHONY: ollama
ollama:
	@ollama serve

.PHONY: start
start:
	docker compose up --build

.PHONY: stop
stop:
	docker compose down --remove-orphans --volumes
	docker image prune -f
