from confluent_kafka import Producer
import logging
import time

# Constants for readability and maintainability
CONST_BOOTSTRAP_SERVERS_IDENTIFIER_STR = "bootstrap.servers"
CONST_DEFAULT_BATCH_COUNT = 100


class kafka_producer:
    """
    Kafka producer class for publishing messages to a Kafka cluster.

    Args:
        bootstrap_servers (str): Comma-separated list of Kafka broker host:port pairs.
        batch_count (int, optional): Maximum number of messages to batch before sending. Defaults to CONST_DEFAULT_BATCH_COUNT.
    """
    def __init__(self, bootstrap_servers, batch_count=CONST_DEFAULT_BATCH_COUNT):
        self.bootstrap_servers = bootstrap_servers
        self.batch_count = batch_count
        self.logger = logging.getLogger("kafka_consumer_log")

        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("kafka %(asctime)-15s %(levelname)-8s %(message)s")
        )
        self.logger.addHandler(handler)

        conf = {CONST_BOOTSTRAP_SERVERS_IDENTIFIER_STR: self.bootstrap_servers}

        self.producer = Producer(conf)

    def delivery_callback(self, err, message) ->None:
        """
        Callback function for message delivery.

        Args:
            err (Error or None): Error if delivery failed, None otherwise.
            message (Message): The produced message.
        """
        if err:
            self.logger.info("Delivery failed for : %s" % err)
        else:
            msg = "Message delivered to [{msg1}] [{msg2}]".format(
                msg1=message.topic(), msg2=message.partition()
            )
            self.logger.info(msg)

    def publish_messages_sync(self, topic, messages, grace_period) ->None:
        """
        Publishes messages to a Kafka topic synchronously with batching and grace period.

        Args:
            topic (str): The Kafka topic to publish messages to.
            messages (list): List of messages to be published.
            grace_period (float): Time to wait after sending a batch before sending the next batch.
        """
        counter = 0
        for message in messages:
            if counter >= self.batch_count:
                self.producer.flush()
                time.sleep(grace_period)

            self.producer.produce(
                topic, str(message), on_delivery=self.delivery_callback
            )

            counter+=1

        self.producer.flush() # Flush any remaining messages