from kafka.kafka_producer import kafka_producer
import os

import json
from flask import Flask, Response
import io

from scrapper.scrapper import Scrapper

app = Flask(__name__)

def main():
    """
    Main function to scrape data, produce to Kafka, and save to a JSON file.

    1. Retrieves Kafka bootstrap servers and topic from environment variables.
    2. Creates a Kafka producer instance.
    3. Creates a Scrapper instance and scrapes data.
    4. Publishes scraped data to Kafka topic.
    5. Saves scraped data to a JSON file.
    """
    bootstrap_servers_address = os.environ.get("bootstrap_servers")
    print(bootstrap_servers_address)
    topic = os.environ.get("topic")

    producer = kafka_producer(
        bootstrap_servers=bootstrap_servers_address, batch_count=1
    )
    scrapper = Scrapper("https://scrapeme.live/shop/")
    scrapped_json = scrapper.call()

    producer.publish_messages_sync(topic=topic, grace_period=1, messages=scrapped_json)

    with open("data.json", "w", encoding="utf8") as file:
        json.dump(scrapped_json, file, indent=4, ensure_ascii=False)
    
main()

@app.route("/")
def streamed_proxy():
    """
    Flask endpoint to stream the contents of the data.json file.
    """
    file = "data.json"
    streaming_file = io.open(
        file,
        mode="r",
        buffering=-1,
        encoding="utf-8",
        errors=None,
        newline=None,
        closefd=True,
    )
    return Response(streaming_file, content_type="application/json")
