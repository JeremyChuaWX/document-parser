# Document Parser

## Dependencies

- Make
- Docker
- Ollama

## Setup

- Copy `.env.example` and rename it to `.env`

- Run this command to setup the project

  ```bash
  make setup
  ```

  - Creates the following directories at the project root
    - `ARTIFACTS_PATH=./artifacts/`
    - `OUTPUTS_PATH=./outputs/`
    - Can be edited in `.env`

- Obtain a copy of the LOINC and store it as a CSV at the following path

  ```
  ./scripts/vector_db_migrate/artifacts/loinc.csv
  ```

- Run this command to initialise the SQL and vector databases

  ```bash
  make migrate
  ```

## Usage

1. Start Ollama server

   ```bash
   make ollama
   ```

2. Run the pipeline

   ```bash
   FILENAME="example.pdf" make start
   ```

   Each step in the pipeline is logged to
   `<OUTPUTS_PATH>/<filename>_<timestamp>/<name-of-step>.log`

3. Clean up the containers and volumes

   ```bash
   make stop
   ```
