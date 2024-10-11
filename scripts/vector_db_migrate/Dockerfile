FROM python

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

COPY artifacts/ .

CMD python3 -u main.py
