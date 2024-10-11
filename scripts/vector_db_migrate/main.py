import pandas as pd
import chromadb
import os

CHROMA_HOST = os.environ["CHROMA_HOST"]
CHROMA_COLLECTION = os.environ["CHROMA_COLLECTION"]

FILE_PATH = "loinc.csv"
COLUMNS = ["LOINC_NUM", "LONG_COMMON_NAME", "EXAMPLE_UNITS"]
BATCH_SIZE = 100


def main():
    client = chromadb.HttpClient(host=CHROMA_HOST)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION)

    if collection.count() > 0:
        print("collection is not empty")
        return

    batches = pd.read_csv(FILE_PATH, usecols=COLUMNS, chunksize=BATCH_SIZE)

    def process_batch(batch):
        batch["combined"] = batch.apply(
            lambda row: f"{row['LONG_COMMON_NAME']}. Unit: {row['EXAMPLE_UNITS']}",
            axis=1,
        )
        collection.add(
            documents=batch["combined"].tolist(),
            ids=batch["LOINC_NUM"].tolist(),
        )

    for batch in batches:
        process_batch(batch)
        print("batch processed", collection.count())

    print("collection populated")


if __name__ == "__main__":
    main()
