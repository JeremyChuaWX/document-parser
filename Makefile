ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: ollama
ollama:
	@ollama serve
