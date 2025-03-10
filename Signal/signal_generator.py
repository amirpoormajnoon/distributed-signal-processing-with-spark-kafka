from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from collections import deque
from kafka import KafkaProducer
import json

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 pyspark-shell'

spark = SparkSession.builder \
    .appName("Kafka-Spark-Consumer") \
    .getOrCreate()

kafka_bootstrap_servers = '192.168.86.12:9092'
kafka_topic = 'xrp_usd_topic'
output_topic = 'signal_topic'
consumer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(value AS STRING)").alias("value")
df = df.withColumn("price", col("value").cast("float")).select("price")

queue_size = 14
data_queue = deque(maxlen=queue_size)
prev_short_ma = None
prev_long_ma = None

def moving_average(data, window_size):
    data_list = list(data)
    return sum(data_list[-window_size:]) / window_size if len(data) >= window_size else None

def exponential_moving_average(data, window_size):
    alpha = 2 / (window_size + 1)
    data_list = list(data)
    ema = data_list[0]
    for price in data_list[1:]:
        ema = (price * alpha) + (ema * (1 - alpha))
    return ema

def calculate_rsi(data):
    gains = [max(data[i] - data[i-1], 0) for i in range(1, len(data))]
    losses = [max(data[i-1] - data[i], 0) for i in range(1, len(data))]
    avg_gain = sum(gains) / len(data)
    avg_loss = sum(losses) / len(data)
    if avg_loss == 0:
        return 100  
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def process_batch(batch_df, batch_id):
    global data_queue, prev_short_ma, prev_long_ma
    signal_array = []
    batch_data = batch_df.toPandas()
    for price in batch_data["price"]:
        data_queue.append(price)
        if len(data_queue) < queue_size:
            continue
        short_ma = moving_average(data_queue, 3)
        long_ma = moving_average(data_queue, 5)
        ema = exponential_moving_average(data_queue, 5)
        rsi = calculate_rsi(data_queue)
        signal_array.append(f"RSI is :{rsi}")
        
        if ema is not None and len(data_queue) >= 2:
            previous_price = list(data_queue)[-2]
            current_price = list(data_queue)[-1]
            if previous_price <= ema and current_price > ema:             
                signal_array.append("Buy with EMA")
            elif previous_price >= ema and current_price < ema:
                
                signal_array.append("Sell with EMA")
            else :
                
                signal_array.append("None with EMA")
        if short_ma and long_ma and rsi is not None:
            if prev_short_ma is not None and prev_long_ma is not None:
                if prev_short_ma <= prev_long_ma and short_ma > long_ma:
                    
                    signal_array.append("Buy with MA")
                elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
                    
                    signal_array.append("Sell with MA")
                else :
                    
                    signal_array.append("None with MA")
            print(signal_array)
            signal_json = json.dumps(signal_array)
            consumer.send(output_topic, value=signal_json.encode('utf-8'))  
            signal_array.clear()
            prev_short_ma = short_ma
            prev_long_ma = long_ma

query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()
