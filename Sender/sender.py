from kafka import KafkaConsumer
import socket
import json

kafka_bootstrap_servers = '192.168.86.12:9092'
input_topic = 'signal_topic'

server_ip = '192.168.1.101'
server_port = 12345

consumer = KafkaConsumer(
    input_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    group_id='signal_group',
    auto_offset_reset='earliest'
)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

for message in consumer:
    signal_data = message.value.decode('utf-8')
    client_socket.send(signal_data.encode('utf-8'))

client_socket.close()
