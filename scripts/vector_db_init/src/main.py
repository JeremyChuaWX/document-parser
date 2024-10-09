import pandas as pd
import chromadb

FILE_PATH = "C:/Users/brand/OneDrive/Documents/BT4103/Loinc.csv"
COLUMNS = ["LOINC_NUM", "LONG_COMMON_NAME", "EXAMPLE_UNITS"]
COLLECTION_NAME = "loinc_embeddings"
BATCH_SIZE = 100


def main():
    client = chromadb.HttpClient(host="vector_db")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

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

    print("collection populated")


if __name__ == "__main__":
    main()
