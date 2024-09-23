from pypdf import PdfReader
from ollama import Client


class Pipelines:
    def __init__(self, document_path: str, ollama_address: str) -> None:
        self.document_path = document_path
        self.document = PdfReader(document_path)
        self.ollama = Client(host=ollama_address)

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

    def extract_text_paginated(self) -> list[str]:
        return [
            page.extract_text(
                extraction_mode="layout",
                layout_mode_scale_weight=1.0,
            )
            for page in self.document.pages
        ]

    def find_tables(self, raw_text: str):
        prompt = f"""
        {raw_text}
        """
        return self.ollama.generate(
            model="hermes3:8b",
            prompt=prompt,
        )

    def filter_information(self, tables: str):
        prompt = f"""
        {tables}
        """
        return self.ollama.generate(
            model="hermes3:8b",
            prompt=prompt,
        )
