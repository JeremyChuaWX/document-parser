import pipeline
from environment import Environment


def main():
    raw_text = pipeline.extract_text(Environment.DOCUMENT_PATH)


if __name__ == "__main__":
    main()
