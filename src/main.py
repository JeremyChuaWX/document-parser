from pipeline import Pipeline
from environment import Environment


def main():
    pipeline = Pipeline(
        Environment.DOCUMENT_PATH,
        Environment.OLLAMA_ADDRESS,
        Environment.OLLAMA_MODEL,
    )
    raw_text = pipeline.extract_text()
    tables = pipeline.find_tables(raw_text)
    filtered = pipeline.filter_information(tables)
    formatted = pipeline.format_information(filtered)


if __name__ == "__main__":
    main()
