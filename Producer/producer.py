import websocket
import json
from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers='192.168.86.12:9092')


pairs_topics = {
    "SOL/USD": "sol_usd_topic",
    "ETH/USD": "eth_usd_topic",
    "XRP/USD": "xrp_usd_topic"
}

KRAKEN_WS_URL = "wss://ws.kraken.com"


def on_message(ws, message):
    data = json.loads(message)
    if isinstance(data, dict) and data.get('event') == 'heartbeat':
        return
    if isinstance(data, list) and len(data) > 1:
        pair_index = data[3]
        if pair_index in pairs_topics:
            topic_name = pairs_topics[pair_index]
            if isinstance(data[1], dict) and 'c' in data[1]:
                last_trade_price = data[1]['c'][0]
                print(f"Last trade price for {pair_index}:", last_trade_price)
                producer.send(topic_name, value=last_trade_price.encode('utf-8'))


def on_open(ws):
    print("Connection opened")
    for pair in pairs_topics.keys():
        subscribe_message = {
            "event": "subscribe",
            "pair": [pair],
            "subscription": {"name": "ticker"}
        }
        ws.send(json.dumps(subscribe_message))


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")
ws = websocket.WebSocketApp(
    KRAKEN_WS_URL,
    on_message=on_message,
    on_open=on_open,
    on_close=on_close
)


ws.run_forever()

