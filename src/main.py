from pipeline import Pipeline


def main():
    pipeline = Pipeline()
    raw_text = pipeline.extract_text()
    tables = pipeline.find_tables(raw_text)
    filtered = pipeline.filter_information(tables)
    formatted = pipeline.format_information(filtered)


if __name__ == "__main__":
    main()
