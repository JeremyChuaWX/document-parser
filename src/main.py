from pipeline import Pipeline


def main():
    print("running document parser pipeline...")

    pipeline = Pipeline()

    pages = pipeline.extract_text_paginated()

    report = pipeline.find_report_info(pages[0])
    print("report\n\n", report, "\n\n")
    report_id = pipeline.insert_report(report)
    print("report_id:", report_id, "\n\n")

    tables = pipeline.find_tables(pages[0])
    tables_dataframe = pipeline.to_dataframe(tables)
    print(tables_dataframe.head())

    for test in tables_dataframe:
        loinc = pipeline.query_loinc(test)
        pipeline.insert_test(test, loinc)
        break


if __name__ == "__main__":
    main()
