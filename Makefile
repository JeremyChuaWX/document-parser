include .env
export

.PHONY: ollama
ollama:
	@ollama serve

.PHONY: start
start:
	docker compose up --build

.PHONY: stop
stop:
	docker compose down --remove-orphans --volumes
