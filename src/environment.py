import os


class Environment:
    ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
    OUTPUTS_PATH = os.environ["OUTPUTS_PATH"]
    FILENAME = os.environ["FILENAME"]
    OLLAMA_ADDRESS = os.environ["OLLAMA_ADDRESS"]
    OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]
    CHROMA_HOST = os.environ["CHROMA_HOST"]
    CHROMA_COLLECTION = os.environ["CHROMA_COLLECTION"]
    POSTGRES_ADDRESS = os.environ["POSTGRES_ADDRESS"]
    DOCUMENT_PATH = os.path.join(ARTIFACTS_PATH, FILENAME)
