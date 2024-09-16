FROM python

RUN apt-get update

RUN apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-chi-sim \
    libtesseract-dev \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN tesseract --list-langs

RUN pip install "unstructured[local-inference,pdf]"

WORKDIR /app

COPY . .

CMD python3 main.py
