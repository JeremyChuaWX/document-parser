import json
import os
from datetime import datetime

from unstructured.partition.pdf import partition_pdf

ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
OUTPUTS_PATH = os.environ["OUTPUTS_PATH"]
FILENAME = os.environ["FILENAME"]
TABLE_CATEGORY = "<class 'unstructured.documents.elements.Table'>"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
document_path = os.path.join(ARTIFACTS_PATH, FILENAME)
output_path = os.path.join(OUTPUTS_PATH, f"{FILENAME}_{timestamp}_output.json")

elements = partition_pdf(
    document_path,
    strategy="hi_res",
    infer_table_structure=True,
    languages=["chi_sim", "eng"],
)

category_counts = {}

tables = []

for element in elements:
    category = str(type(element))
    if category in category_counts:
        category_counts[category] += 1
    else:
        category_counts[category] = 1
    if category == TABLE_CATEGORY:
        tables.append(element)

print("\n\n", category_counts)

res = {"tables": []}
for table in tables:
    res["tables"].append(
        {
            "text": table.text,
            "html": table.metadata.text_as_html,
        }
    )

with open(output_path, "w") as f:
    json.dump(res, f)
