from pipeline import Pipeline


def main():
    print("running document parser pipeline...")
    pipeline = Pipeline()
    raw_text = pipeline.extract_text()
    tables = pipeline.find_tables(raw_text)
    formatted = pipeline.format_tables(tables)
    # filtered = pipeline.filter_information(tables)


if __name__ == "__main__":
    main()
