FILENAME ?= $(error FILENAME is not set. Use 'make run FILENAME=...')
ARTIFACTS_PATH ?= "./artifacts"
OUTPUTS_PATH ?= "./outputs"
OLLAMA_ADDRESS ?= "host.docker.internal:3000"
.PHONY: run
run:
	@echo "running docker container..."
	@docker run --rm -it \
		-e FILENAME=$(FILENAME) \
		-e ARTIFACTS_PATH=$(ARTIFACTS_PATH) \
		-e OUTPUTS_PATH=$(OUTPUTS_PATH) \
		-e OLLAMA_ADDRESS=$(OLLAMA_ADDRESS) \
		-v $(ARTIFACTS_PATH):/app/artifacts \
		-v $(OUTPUTS_PATH):/app/outputs \
	$$(docker build -q .)
