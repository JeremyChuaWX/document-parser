import gc
from pipeline import Pipeline


def main():
    print("running document parser pipeline...")

    pipeline = Pipeline()

    pages = pipeline.extract_text_paginated()

    report = pipeline.find_report_info(pages[0])
    print("report\n\n", report, "\n\n")
    report_id = pipeline.insert_report(report)
    print("report_id:", report_id, "\n\n")

    for page in pages:
        tables = pipeline.find_tables(page)
        tables_dataframe = pipeline.to_dataframe(tables)
        print(tables_dataframe.head())

        for _, test in tables_dataframe.iterrows():
            print("test", test)
            loinc = pipeline.query_loinc(test)
            print("loinc", loinc)
            pipeline.insert_test(test, report_id, loinc)

        del tables, tables_dataframe
        gc.collect()


if __name__ == "__main__":
    main()
