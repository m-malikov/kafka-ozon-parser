USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
FETCH_PAGES = 5
BASE_URL = "https://api.ozon.ru/composer-api.bx/page/json/v1"

import socket

KAFKA_CONF = {
    "bootstrap.servers": "broker:9092",
    "client.id": socket.gethostname()
}
KAFKA_TOPIC = "ozon-category"
