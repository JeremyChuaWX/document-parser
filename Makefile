include .env
export

.PHONY: ollama
ollama:
	@ollama serve

.PHONY: start
start:
	docker compose up --build -d

.PHONY: stop
stop:
	docker compose down --remove-orphans --volumes
	docker image prune -f
