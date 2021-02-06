import logging
import json

from confluent_kafka import Consumer, Producer, KafkaError, KafkaException

import config


def parse_items(data):
    data = json.loads(data)
    data = data["catalog"]["searchResultsV2"]
    data = next(iter(data.values()))["items"]

    def record_to_item(record):
        record = record["cellTrackingInfo"]
        return {
            "id": record["id"],
            "name": record["title"],
            "price": record["price"],
            "discount": record["discount"]
        }

    return list(map(record_to_item, data))


def write_items(items, producer, logger):
    def acked(err, msg):
        if err is not None:
            logger.error("Failed to deliver message: {}: {}".format(err, msg))
        else:
            logger.info("Message produced: {}".format(msg))

    for item in items:
        producer.produce(
            config.KAFKA_OUT_TOPIC,
            value=json.dumps(item),
            callback=acked
        )


def process_message(message, producer, logger):
    value = message.value()
    _, timestamp = message.timestamp()

    try:
        items = parse_items(value)
    except Exception as e:
        logger.error("Error parsing items: " + repr(e))
        return

    for item in items:
        item.update({"timestamp": timestamp})

    try:
        write_items(items, producer, logger)
    except Exception as e:
        logger.error("Error writing to topic: " + repr(e))


def consume_loop(consumer, producer, logger):
    try:
        consumer.subscribe([config.KAFKA_IN_TOPIC])
        while True:
            try:
                msg = consumer.poll(timeout=1.0)
                producer.poll(0)
            except Exception as e:
                logger.exception(e)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.warning("{} {} reached end at offset {}".format(
                        msg.topic(), msg.partition(), msg.offset()))

                elif msg.error():
                    logger.exception(KafkaException(msg.error()))
            else:
                logger.error("Received message {} {} at offset {}".format(
                    msg.topic(), msg.partition(), msg.offset()))
                process_message(msg, producer, logger)
    finally:
        consumer.close()


def main():
    consumer = Consumer(config.KAFKA_CONSUMER_CONF)
    producer = Producer(config.KAFKA_PRODUCER_CONF)
    logger = logging.Logger(config.HOSTNAME, level=logging.INFO)
    consume_loop(consumer, producer, logger)


if __name__ == "__main__":
    main()
