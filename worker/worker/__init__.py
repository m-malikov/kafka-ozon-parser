from flask import Flask, request

from worker.ozon_requests import get_category_data
from worker.kafka import init_kafka, write_to_topic


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    init_kafka(app.config["KAFKA_CONF"])

    @app.route("/", methods=["GET"])
    def process_category():
        if "url" not in request.args:
            return "Argument 'url' is expected", 400

        try:
            category_data = get_category_data(request.args["url"])
        except Exception as e:
            app.logger.exception(e)
            return "Error retreiving category: " + repr(e), 500

        try:
            write_to_topic(category_data, app.config["KAFKA_TOPIC"], app.logger)
        except Exception as e:
            app.logger.exception(e)
            return "Error sending to Kafka: " + repr(e), 500

        return "OK", 200

    return app
