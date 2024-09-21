import json
import os
from datetime import datetime

from ollama import Client

ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
OUTPUTS_PATH = os.environ["OUTPUTS_PATH"]
FILENAME = os.environ["FILENAME"]
OLLAMA_ADDRESS = os.environ["OLLAMA_ADDRESS"]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
document_path = os.path.join(ARTIFACTS_PATH, FILENAME)
output_path = os.path.join(OUTPUTS_PATH, f"{FILENAME}_{timestamp}_output.json")
client = Client(host=OLLAMA_ADDRESS)


def query(text, html):
    prompt = f"""
    SKIBIDI RIZZ, I AM DAWAE. You are an excellent specimen.

    I have extracted a table from a PDF document.

    This is the table in HTML:
    ```
    {html}
    ```

    This is the table as raw text:
    ```
    {text}
    ```

    The text in the HTML is inaccurate.
    Using the raw text as the source of truth, replace the text inside the HTML table elements with the respective snippets.

    Return ONLY the modified HTML. I will KILL MYSELF if you don't only return HTML.
    """
    return client.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )["message"]["content"]


tables = None

with open(document_path, "r") as f:
    tables = json.loads(f.read())["tables"]

responses = {
    "responses": [query(table["text"], table["html"]) for table in tables],
}

with open(output_path, "w") as f:
    f.write(json.dumps(responses))
