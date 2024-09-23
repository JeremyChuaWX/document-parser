import json
import os
from datetime import datetime

import unstructured_client
from unstructured_client.models import operations, shared

API_KEY = os.environ["UNSTRUCTURED_API_KEY"]
API_URL = os.environ["UNSTRUCTURED_API_URL"]
ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
OUTPUTS_PATH = os.environ["OUTPUTS_PATH"]
FILENAME = os.environ["FILENAME"]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
input_path = os.path.join(ARTIFACTS_PATH, FILENAME)
output_path = os.path.join(OUTPUTS_PATH, f"{FILENAME}_{timestamp}_output.json")

client = unstructured_client.UnstructuredClient(
    api_key_auth=API_KEY,
    server_url=API_URL,
)

with open(input_path, "rb") as f:
    files = shared.Files(
        content=f.read(),
        file_name=input_path,
    )

req = operations.PartitionRequest(
    partition_parameters=shared.PartitionParameters(
        files=files,
        strategy=shared.Strategy.HI_RES,
        languages=["chi_sim", "eng"],
        split_pdf_concurrency_level=15,
    ),
)

try:
    res = client.general.partition(request=req)
    element_dicts = [element for element in res.elements]

    # Print the processed data's first element only.
    print(element_dicts[0])

    # Write the processed data to a local file.
    json_elements = json.dumps(element_dicts, indent=2)

    with open(output_path, "w") as f:
        f.write(json_elements)
except Exception as e:
    print(e)
