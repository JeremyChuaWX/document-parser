import os
from datetime import datetime

from ollama import Client
from pypdf import PdfReader

from environment import Environment


class Pipeline:
    def __init__(self) -> None:
        self.document = PdfReader(Environment.DOCUMENT_PATH)
        self.ollama = Client(host=Environment.OLLAMA_ADDRESS)
        self.ollama.pull(Environment.OLLAMA_MODEL)

    def extract_text(self):
        res = "\n\n".join(
            [
                page.extract_text(
                    extraction_mode="layout",
                    layout_mode_scale_weight=1.0,
                )
                for page in self.document.pages
            ]
        )
        self._save("extract_text", res)
        return res

    def extract_text_paginated(self) -> list[str]:
        res = [
            page.extract_text(
                extraction_mode="layout",
                layout_mode_scale_weight=1.0,
            )
            for page in self.document.pages
        ]
        self._save("extract_text_paginated", res)
        return res

    def find_tables(self, raw_text: str):
        prompt = f"""
        {raw_text}
        """
        res = self._generate(prompt)
        self._save("find_tables", res["response"])
        return res

    def filter_information(self, tables: str):
        prompt = f"""
        {tables}
        """
        res = self._generate(prompt)
        self._save("find_tables", res["response"])
        return res

    def format_information(self, filtered: str):
        prompt = f"""
        {filtered}
        """
        res = self._generate(prompt)
        self._save("find_tables", res["response"])
        return res

    def _save(self, name: str, data):
        file = os.path.join(
            Environment.OUTPUTS_PATH,
            f"{Environment.FILENAME.split(".")[0]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}",
            f"{name}.log",
        )
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as f:
            f.write(data)

    def _generate(self, prompt):
        return self.ollama.generate(
            model=Environment.OLLAMA_MODEL,
            prompt=prompt,
        )
