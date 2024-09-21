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
output_path = os.path.join(
    OUTPUTS_PATH, f"{FILENAME.split(".")[0]}_{timestamp}_output.json"
)
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
    Using the raw text as the source of truth, replace the text inside `<td></td>` tags with the respective snippets from the raw text.
    Do not change the table structure. Do not modify any HTML tags. Only replace the text between `<td></td>` tags.
    Return the final HTML after performing the replacements. Do not say any thing else before or after.
    I will KILL MYSELF if you don't only return HTML.

    Example:

    ```input
    <table><tbody><td></td><td></td><td>"inaccurate text from HTML"</td>...</tbody></table>
    ```

    ```output
    <table><tbody><td></td><td></td><td>"accurate text from raw text"</td>...</tbody></table>
    ```
    """
    response = client.generate(
        model="hermes3:8b",
        prompt=prompt,
    )["response"]
    print(html, "\n\n", response, "\n\n")
    return response


tables = None

with open(document_path, "r") as f:
    tables = json.loads(f.read())["tables"]

# responses = {
#     "responses": [query(table["text"], table["html"]) for table in tables],
# }

responses = {"responses": query(tables[0]["text"], tables[0]["html"])}

with open(output_path, "w") as f:
    f.write(json.dumps(responses))
