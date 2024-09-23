# PDF parsing

Make `artifacts` and `outputs` directories for inputs and outputs. These directories are gitignored.

Build and run the docker image with the required environment variables.

```bash
make run FILENAME=... ARTIFACTS_PATH=... OUTPUTS_PATH=...
```

The output is a JSON with the format:

```json
{
    "tables": [
        {
            "text": "...",
            "html": "..."
        }
    ]
}
```
