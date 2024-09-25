import os
from datetime import datetime

from ollama import Client
from pypdf import PdfReader

from environment import Environment


class Pipeline:
    def __init__(self) -> None:
        self.document = PdfReader(Environment.DOCUMENT_PATH)
        self.ollama = Client(host=Environment.OLLAMA_ADDRESS)
        self.save_dir = os.path.join(
            Environment.OUTPUTS_PATH,
            f"{Environment.FILENAME.split(".")[0]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}",
        )

        self.ollama.pull(Environment.OLLAMA_MODEL)
        os.makedirs(self.save_dir, exist_ok=True)

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

    def extract_text_paginated(self):
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

        Your task:
        - Find and return all tables in the raw text
        - Delimit tables with triple quotes
        - Do not include any summary or other explanations
        - Do not modify the raw text except removing all chinese characters

        Take note:
        - Ensure tables have header rows

        Output format:
        '''
        <table 1>
        '''

        '''
        <table 2>
        '''
        """
        res = self._generate(prompt)
        self._save("find_tables", res)
        return res

    def format_tables(self, tables: str):
        prompt = f"""
        The following are multiple tables delimited by triple quotes:

        {tables}

        They have the following format:
        '''
        <table 1>
        '''

        '''
        <table 2>
        '''

        Your task:
        - Convert the tables into CSV format
        - Make the first row the header row
        - Reorder columns based on the header row
        - Do not include any summary or other explanations

        Your example output:
        '''
        <csv of table 1>
        '''

        '''
        <csv of table 2>
        '''
        """
        res = self._generate(prompt)
        self._save("format_tables", res)
        return res

    def filter_tables(self, tables: str):
        prompt = f"""
        {tables}
        """
        res = self._generate(prompt)
        self._save("filter_tables", res)
        return res

    def query_loinc(self, formatted: str):
        # NOTE: `formatted` should be some sort of structured format (csv, json, ...)
        # TODO: parses `formatted`, queries for LOINC in vector DB, returns formatted + LOINC
        pass

    def insert_records(self, loinc: str):
        # NOTE: `loinc` should be some sort of structured format (csv, json, ...)
        # TODO: parses `loinc`, save each row to relational DB
        pass

    def _save(self, name: str, data: str):
        file = os.path.join(self.save_dir, f"{name}.log")
        with open(file, "w") as f:
            f.write(data)
            print(f"saved: {file}")

    def _generate(self, prompt: str, json=False):
        return self.ollama.generate(
            model=Environment.OLLAMA_MODEL,
            prompt=prompt,
            format="json" if json else "",
            options={
                "temperature": 0.0,
            },
        )["response"]
