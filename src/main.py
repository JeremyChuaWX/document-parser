from pipeline import Pipeline


def main():
    print("running document parser pipeline...")
    pipeline = Pipeline()
    pages = pipeline.extract_text_paginated()
    tables = pipeline.find_tables(pages[0]) # swap to for loop to process all pages
    formatted = pipeline.format_tables(tables)
    parsed = pipeline.parse_tables(formatted)
    dataframes = pipeline.to_dataframes(parsed)


if __name__ == "__main__":
    main()
