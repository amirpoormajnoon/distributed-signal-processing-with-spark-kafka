FROM python:3.9-slim

RUN pip install kafka-python

COPY . /app

WORKDIR /app

CMD ["python", "sender.py"]
