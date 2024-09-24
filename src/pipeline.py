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
        The following is raw text extracted from a medical PDF:
        ```text
        {raw_text}
        ```

        Task:
        Find and return all the tables in the raw text.

        Response JSON format:
        ```json
        {{
            "tables": [
                "<raw text of table>",
                "<raw text of table>"
            ]
        }}
        ```
        """
        res = self._generate(prompt)
        self._save("find_tables", res["response"])
        return res

    def filter_information(self, tables: str):
        prompt = f"""
        {tables}
        """
        res = self._generate(prompt)
        self._save("filter_information", res["response"])
        return res

    def format_information(self, filtered: str):
        prompt = f"""
        {filtered}
        """
        res = self._generate(prompt)
        self._save("format_information", res["response"])
        return res

    def query_loinc(self, formatted: str):
        # NOTE: `formatted` should be some sort of structured format (csv, json, ...)
        # TODO: parses `formatted`, queries for LOINC in vector DB, returns formatted + LOINC
        pass

    def insert_records(self, loinc: str):
        # NOTE: `loinc` should be some sort of structured format (csv, json, ...)
        # TODO: parses `loinc`, save each row to relational DB
        pass

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
            format="json",
            options={
                "temperature": 0.0,
            },
        )
