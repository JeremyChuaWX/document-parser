import json
import os
from datetime import datetime
from functools import wraps

import chromadb
import ollama
import pandas as pd
import pymysql
from pypdf import PdfReader
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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
        pymysql.install_as_MySQLdb()

        self.document = PdfReader(Environment.DOCUMENT_PATH)

        self.ollama = ollama.Client(host=Environment.OLLAMA_ADDRESS)
        self.ollama.pull(Environment.OLLAMA_MODEL)

        self.collection = chromadb.HttpClient(
            host=Environment.CHROMA_HOST,
        ).get_collection(
            Environment.CHROMA_COLLECTION,
        )

        self.session = sessionmaker(
            bind=create_engine(
                Environment.MYSQL_ADDRESS,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600,
                connect_args={"connect_timeout": 5},
            )
        )

        self.save_dir = os.path.join(
            Environment.OUTPUTS_PATH,
            f"{Environment.FILENAME.split(".")[0]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}",
        )
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
        You are part of a data processing pipeline.

        The following is a page of raw text extracted from a medical PDF:

        ```text
        {raw_text}
        ```

        Your task:
        - Find and return all tables in the raw text
        - Find the titles that summarise the contents of the tables
        - Return all columns and rows in the tables
        - Do not include any summary or other explanations
        - Do not modify the raw text except removing all chinese characters

        Take note:
        - Ensure tables have header rows
        - I am looking for tables that contain measurements of patients
        - Do not hallucinate or generate any text, only take lines from the raw text

        Output format:

        '''
        <title for table 1>

        <table 1>
        '''

        '''
        <title for table 2>

        <table 2>
        '''
        """
        return self._generate(prompt)

    @save_output
    def format_tables(self, tables: str):
        prompt = f"""
        You are part of a data processing pipeline.

        The following are multiple tables delimited by triple quotes:

        {tables}

        They have the following format:
        '''
        <title for table 1>

        <table 1>
        '''

        '''
        <title for table 2>

        <table 2>
        '''

        Your task:
        - Convert the tables into CSV format
        - Make the first row the header row
        - Reorder columns based on the header row
        - Do not include any summary or other explanations

        Output format:
        '''
        <title for table 1>

        <csv of table 1>
        '''

        '''
        <title for table 2>

        <csv of table 2>
        '''
        """
        return self._generate(prompt)

    @save_output
    def parse_tables(self, tables: str):
        prompt = f"""
        You are part of a data processing pipeline.

        The following are multiple tables delimited by triple quotes:

        {tables}

        They have the following format:
        '''
        <title for table 1>

        <csv of table 1>
        '''

        '''
        <title for table 2>

        <csv of table 2>
        '''

        Your task:
        - Return the tables in JSON format described below
        - Do not include any summary or other explanations

        JSON format:
        {{
            "tables": [
                {{
                    "title": "<title for table 1>",
                    "table": [
                        [...],
                        [...],
                        ...
                    ]
                }},
                {{
                    "title": "<title for table 2>",
                    "table": [
                        [...],
                        [...],
                        ...
                    ]
                }},
                ...
            ]
        }}
        """
        return self._generate(prompt, json=True)

    def to_dataframes(self, tables: str):
        dfs = json.loads(tables)["tables"]
        for df in dfs:
            df["table"] = pd.DataFrame(df["table"])
        return dfs

    def query_loinc(self, category: str, test: str, unit: str) -> str:
        """
        Combine metadata of an extracted row from a table and query the vector database for the associated LOINC.
        """
        query = f"{category},{test}. Units: {unit}"
        result = self.collection.get(query)  # TODO: fix this
        return result

    def insert_records(self, loinc: str, data: str):
        # TODO: insert report, insert tests
        sql_query = text("%s")
        with self.session() as session:
            session.execute(sql_query, [loinc, data])
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
