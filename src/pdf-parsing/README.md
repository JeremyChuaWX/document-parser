Example PDF parsing using Unstructured.

Build and run the docker image with the document path as variable.

```bash
docker run --rm -it -e DOCUMENT_PATH="<path/to/document>" $(docker build -q .)
```
