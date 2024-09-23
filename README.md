# Document Parser

## Dependencies

- Docker
- Ollama

## Setup

- Copy `.env.example` and rename to `.env`
- Fill in the appropriate values in `.env`

## Usage

1. Start Ollama server
  ```bash
  make ollama
  ```
2. Run the pipeline
  ```bash
  FILENAME="example.pdf" make start
  ```
  - Each step in the pipeline is logged to `outputs/<filename>_<timestamp>/<name-of-step>.log`
3. Clean up the containers and volumes
  ```bash
  make stop
  ```
