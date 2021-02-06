from confluent_kafka import Producer

producer = None


def init_kafka(kafka_conf):
    global producer
    producer = Producer(kafka_conf)


def write_to_topic(data, topic, logger):
    def acked(err, msg):
        if err is not None:
            logger.error("Failed to deliver message: {}: {}".format(err, msg))
        else:
            logger.error("Message produced: {}".format(msg))

    for page in data:
        producer.produce(topic, value=page, callback=acked)
    producer.poll(0)
