import os
from unstructured.partition.pdf import partition_pdf

DOCUMENT_PATH = os.environ["DOCUMENT_PATH"]

TABLE_CATEGORY = "<class 'unstructured.documents.elements.Table'>"

elements = partition_pdf(
    DOCUMENT_PATH,
    strategy="hi_res",
    infer_table_structure=True,
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

print(category_counts)

print("\n\n".join([table.metadata.text_as_html for table in tables]))
