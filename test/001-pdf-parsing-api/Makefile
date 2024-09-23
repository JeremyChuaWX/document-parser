FILENAME ?= $(error FILENAME is not set. Use 'make run FILENAME=... ARTIFACTS_PATH=... OUTPUTS_PATH=...')
ARTIFACTS_PATH ?= $(error ARTIFACTS_PATH is not set. Use 'make run FILENAME=... ARTIFACTS_PATH=... OUTPUTS_PATH=...')
OUTPUTS_PATH ?= $(error OUTPUTS_PATH is not set. Use 'make run FILENAME=... ARTIFACTS_PATH=... OUTPUTS_PATH=...')
.PHONY: run
run:
	@echo "running docker container..."
	@docker run --rm -it \
		-e ARTIFACTS_PATH=$(ARTIFACTS_PATH) \
		-e OUTPUTS_PATH=$(OUTPUTS_PATH) \
		-e FILENAME=$(FILENAME) \
		--env-file .env \
		-v $(ARTIFACTS_PATH):/app/artifacts \
		-v $(OUTPUTS_PATH):/app/outputs \
	$$(docker build -q .)
