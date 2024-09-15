FROM python

RUN apt-get update

RUN apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "unstructured[pdf]"

WORKDIR /app

COPY . .

CMD python3 main.py
