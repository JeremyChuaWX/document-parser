import json
import os
from datetime import datetime

from pypdf import PdfReader

ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
OUTPUTS_PATH = os.environ["OUTPUTS_PATH"]
FILENAME = os.environ["FILENAME"]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
document_path = os.path.join(ARTIFACTS_PATH, FILENAME)
output_path = os.path.join(
    OUTPUTS_PATH, f"{FILENAME.split(".")[0]}_{timestamp}_output.txt"
)

document = PdfReader(document_path)

page_text = document.pages[0].extract_text(
    extraction_mode="layout",
    layout_mode_scale_weight=1.0,
)
