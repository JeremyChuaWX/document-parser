import os
from datetime import datetime


class Environment:
    ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
    OUTPUTS_PATH = os.environ["OUTPUTS_PATH"]
    FILENAME = os.environ["FILENAME"]
    OLLAMA_ADDRESS = os.environ["OLLAMA_ADDRESS"]
    OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]

    DOCUMENT_PATH = os.path.join(ARTIFACTS_PATH, FILENAME)
    OUTPUT_PATH = os.path.join(
        OUTPUTS_PATH,
        f"{FILENAME.split(".")[0]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}_output.txt",
    )
