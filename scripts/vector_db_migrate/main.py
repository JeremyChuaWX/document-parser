import gc
import os

import chromadb
import pandas as pd

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

    for i, batch in enumerate(batches, 1):
        combined = batch.apply(
            lambda row: f"{row['LONG_COMMON_NAME']}. Unit: {row['EXAMPLE_UNITS']}",
            axis=1,
        ).tolist()
        ids = batch["LOINC_NUM"].tolist()
        collection.add(
            documents=combined,
            ids=ids,
        )
        print(f"batch {i} processed, collection count: {collection.count()}")
        del combined, ids, batch
        gc.collect()

    print("collection populated")


if __name__ == "__main__":
    main()
