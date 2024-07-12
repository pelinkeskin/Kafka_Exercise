# Local Kafka Environment Setup
## Purpose:
This Bash script sets up a local Kafka environment using Docker for testing and development purposes. It includes steps to create a Docker network, start Zookeeper and Kafka containers, create a Kafka topic, produce a message, and consume it.

## Prerequisites:
* Docker installed and running.

## Usage:
* Run the script: ```sh task1.sh```
* If ownership error occurs use ```chmod 755 task1.sh``` to run the file as a executable.

## Script Breakdown:
* __Network Creation:__ Creates a Docker network for isolating the containers.
* __Zookeeper Container:__ Starts a Zookeeper container with necessary configurations.
* __Kafka Container:__ Starts a Kafka container, configuring advertised listeners, offsets topic replication factor, and Zookeeper connection.
* __Kafka Topic Creation:__ Creates a Kafka topic named "task1-topic" with 3 partitions.
* __Message Production:__ Sends a message with key "1" and value "task1_message" to the created topic.
* __Message Consumption:__ Consumes messages from the topic with a 10-second timeout.
* __Cleanup:__ Removes the containers and network.

