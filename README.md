# Document Parser

## Dependencies

- Make
- Docker
- Ollama

## Setup

- Run this command to setup the project

  ```bash
  make setup
  ```

  - Creates the following directories at the project root
    - `artifacts/`
    - `outputs/`
  - Copies `.env.example` and renames to `.env`
- Run this command to initialise the vector database with LOINC embeddings

  ```bash
  make vector_db
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

   Each step in the pipeline is logged to `outputs/<filename>_<timestamp>/<name-of-step>.log`

3. Clean up the containers and volumes

   ```bash
   make stop
   ```
