KAFKA_BOOTSTRAP_SERVER = "broker:9092"
KAFKA_CONSUMER_CONF = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVER,
    "group.id": "parser"
}

import socket
HOSTNAME = socket.gethostname()

KAFKA_PRODUCER_CONF = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVER,
    "client.id": HOSTNAME
}

KAFKA_IN_TOPIC = "ozon-category"
KAFKA_OUT_TOPIC = "ozon-products"
