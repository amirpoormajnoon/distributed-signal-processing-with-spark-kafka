FROM python:3.9
RUN apt-get update && apt-get install -y openjdk-17-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
COPY pyspark-3.5.3.tar.gz /app/
RUN pip install --upgrade pip
RUN pip install /app/pyspark-3.5.3.tar.gz kafka-python pandas
COPY . /app
WORKDIR /app
CMD ["python", "signal_generator.py"]
