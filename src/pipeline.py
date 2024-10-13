import json as j
import os
from datetime import datetime
from functools import wraps
from io import StringIO

import chromadb
import ollama
import pandas as pd
from pypdf import PdfReader
from sqlalchemy import create_engine, text

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

        self.ollama = ollama.Client(host=Environment.OLLAMA_ADDRESS)
        self.ollama.pull(Environment.OLLAMA_MODEL)

        self.collection = chromadb.HttpClient(
            host=Environment.CHROMA_HOST,
        ).get_collection(
            Environment.CHROMA_COLLECTION,
        )

        self.engine = create_engine(
            Environment.POSTGRES_ADDRESS,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            connect_args={"connect_timeout": 5},
        )

        self.save_dir = os.path.join(
            Environment.OUTPUTS_PATH,
            f"{Environment.FILENAME.split('.')[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
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
    def find_report_info(self, raw_text: str):
        prompt = f"""
        You are tasked to find metadata from the text extracted from a PDF file. 
        The text contains the results of a patient's laboratory tests.

        Please take note of the following:
        1. The metadata should contain the report_id, lab_name, date_reported, date_imported, patient_age, gender (gender is an enum if values 'M', 'F', 'O')
        2. Results can be text or categorical, such as Negative or Positive or Nil or etc.
        3. For results that are missing, you can fill them with "NULL", but other entries of other columns should be retained.

        The output should look like the following JSON format:

        {{
            "report_id": "XXX",
            "lab_name": "XXX",
            "date_reported": "XXX",
            "date_imported": "XXX",
            "patient_age": "XXX",
            "gender": "M"
        }}

        Respect the following datatypes:

        {{
            "report_id": "VARCHAR",
            "lab_name": "VARCHAR",
            "date_reported": "DATE",
            "date_imported": "DATE",
            "patient_age": "INT",
            "gender": "ENUM('M', 'F', 'O')"
        }}

        Return only the JSON with no additional summary or explanations.

        Here is the text:
        {raw_text}
        """
        return self._generate(prompt, json=True)

    @save_output
    def find_tables(self, raw_text: str):
        prompt = f"""
        You are tasked to store laboratory test results into a csv format based on the text extracted from a PDF file. 
        The text contains the results of a patient's laboratory tests.

        Please take note of the following:
        1. The data should contain the category, subcategory, test, result, unit columns. These values should remain as is. Subcategory can be empty.
        2. There will be values that contain power of 10, keep it as is.
        3. Results can be text or categorical, such as Negative or Positive or Nil or etc.
        4. Some tests would have both absolute (ABS) values and percentage (PCT) values. You should only retain the absolute values.
        5. There would be non-english content, like Chinese as well, these can be ignored.
        6. The category, subcategory, test, result may not be in the correct order in the text.
        7. There is also a possibility that the text may contain errors or missing values.
        8. There is also a possibility that the text may contain multiple categories and subcategories.
        9. There may be letters such as "H" or "L" in front of some values, these should be removed.
        10. For results that are missing, you can fill them with "N/A", but other entries of other columns should be retained.
        11. Reference ranges, which usually have values between 2 parentheses, can be ignored.
        12. If the text does not contain any lab test results, answer nothing. 
        13. You should attach results with their respective units mentioned in the text, if applicable.

        The output should look like the following CSV format:

        category,subcategory,test,result,unit
        HAEMATOLOGY,,Haemogoblin,13.9,g/dL
        LIPIDS,,Total Cholesterol,5.7,mmol/L
        HAEMATOLOGY,Differential Count,Neutrophils,4.76*10^9,/L

        Finally, return only the csv with the following headers:
        "category,subcategory,test,result,unit"
        Return only the csv with no additional summary or explanations.

        Here is the text:
        {raw_text}
        """
        return self._generate(prompt)

    def to_dataframe(self, data: str):
        return pd.read_csv(StringIO(data))

    def query_loinc(self, test) -> str:
        """
        Combine metadata of an extracted row from a table and query the vector database for the associated LOINC.
        """
        query = f"{test['category']},{test['subcategory']},{test['test']}. Units: {test['unit']}"
        return self.collection.query(query_texts=query, n_results=1)["ids"][0][0]

    def insert_report(self, report):
        report = {k: v if v != "NULL" else None for k, v in report.items()}
        sql_query = text("""
        INSERT INTO reports (
            report_id,
            lab_name,
            date_reported,
            date_imported,
            patient_age,
            gender
        ) VALUES (
            :report_id,
            :lab_name,
            :date_reported,
            :date_imported,
            :patient_age,
            :gender
        ) RETURNING
            id
        ;
        """)
        with self.engine.connect() as connection:
            res = connection.execute(sql_query, report)
        return res.fetchone()[0]

    def insert_test(self, test, report_id, loinc):
        sql_query = text("""
        INSERT INTO tests (
            report_id,
            name,
            category,
            subcategory,
            result,
            unit,
            loinc
        ) VALUES (
            :report_id,
            :name,
            :category,
            :subcategory,
            :result,
            :unit,
            :loinc
        ) RETURNING
            id
        ;
        """)
        with self.engine.connect() as connection:
            connection.execute(
                sql_query,
                {
                    "report_id": report_id,
                    "name": test["test"],
                    "category": test["category"],
                    "subcategory": test["subcategory"],
                    "result": test["result"],
                    "unit": test["unit"],
                    "loinc": loinc,
                },
            )

    def _generate(self, prompt: str, json=False):
        response = self.ollama.generate(
            model=Environment.OLLAMA_MODEL,
            prompt=prompt,
            format="json" if json else "",
            options={
                "temperature": 0.0,
            },
        )["response"]
        if json:
            return j.loads(response)
        else:
            return response
