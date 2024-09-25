import os
from datetime import datetime
from functools import wraps

from ollama import Client
from pypdf import PdfReader

from environment import Environment


def save_output(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        file = os.path.join(self.save_dir, f"{func.__name__}.log")
        with open(file, "w") as f:
            f.write(result if isinstance(result, str) else str(result))
            print(f"saved: {file}")
        return result

    return wrapper


class Pipeline:
    def __init__(self):
        self.document = PdfReader(Environment.DOCUMENT_PATH)
        self.ollama = Client(host=Environment.OLLAMA_ADDRESS)
        self.save_dir = os.path.join(
            Environment.OUTPUTS_PATH,
            f"{Environment.FILENAME.split(".")[0]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}",
        )

        self.ollama.pull(Environment.OLLAMA_MODEL)
        os.makedirs(self.save_dir, exist_ok=True)

    @save_output
    def extract_text(self):
        return "\n\n".join(
            [
                page.extract_text(
                    extraction_mode="layout",
                    layout_mode_scale_weight=1.0,
                )
                for page in self.document.pages
            ]
        )

    @save_output
    def extract_text_paginated(self):
        return [
            page.extract_text(
                extraction_mode="layout",
                layout_mode_scale_weight=1.0,
            )
            for page in self.document.pages
        ]

    @save_output
    def find_tables(self, raw_text: str):
        prompt = f"""
        The following is raw text extracted from a medical PDF:
        ```text
        {raw_text}
        ```

        Your task:
        - Find and return tables in the raw text
        - Delimit tables with triple quotes
        - Do not include any summary or other explanations
        - Do not modify the raw text except removing all chinese characters

        Take note:
        - Ensure tables have header rows
        - I am looking for tables that contain measurements and results of patients

        Output format:
        '''
        <table 1>
        '''

        '''
        <table 2>
        '''
        """
        return self._generate(prompt)

    @save_output
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

        Output format:
        '''
        <csv of table 1>
        '''

        '''
        <csv of table 2>
        '''
        """
        return self._generate(prompt)

    @save_output
    def filter_tables(self, tables: str):
        prompt = f"""
        {tables}
        """
        return self._generate(prompt)

    def query_loinc(self, formatted: str):
        # NOTE: `formatted` should be some sort of structured format (csv, json, ...)
        # TODO: parses `formatted`, queries for LOINC in vector DB, returns formatted + LOINC
        pass

    def insert_records(self, loinc: str):
        # NOTE: `loinc` should be some sort of structured format (csv, json, ...)
        # TODO: parses `loinc`, save each row to relational DB
        pass

    def _generate(self, prompt: str, json=False):
        return self.ollama.generate(
            model=Environment.OLLAMA_MODEL,
            prompt=prompt,
            format="json" if json else "",
            options={
                "temperature": 0.0,
            },
        )["response"]
