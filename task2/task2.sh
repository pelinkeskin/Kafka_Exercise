#!/bin/bash

# Define container and network names for consistency
kafka_container=task2_kafka
zookeeper_container=task2_zookeeper
task2_network=task2_network
task2_application=task2_application
task2_application_port=8000
task2_topic=task2-topic

# Create an isolated Docker network for the Kafka environment
docker network create task2_network

# Start Zookeeper container within the created network
docker run \
    --name $zookeeper_container \
    --net=$task2_network \
    -e ZOOKEEPER_CLIENT_PORT=2181 \
    -e ZOOKEEPER_TICK_TIME=2000 \
    -e ZOOKEEPER_SYNC_LIMIT=2 \
    -d confluentinc/cp-zookeeper:7.5.5 

# Wait for Zookeeper to be fully started
until [ "docker inspect -f {{.State.Running}} $zookeeper_container"=="true" ]; do
    sleep 0.1;
done;
sleep 3

# Start Kafka container within the network, configuring necessary settings
docker run \
    --net=$task2_network \
    --name $kafka_container \
    --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://$kafka_container:9092 \
    --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    --env KAFKA_ZOOKEEPER_CONNECT=$zookeeper_container:2181 \
    -d confluentinc/cp-kafka:7.5.5 

# Wait for Kafka to be ready
sleep 5

# Create a Kafka topic with 3 partitions
echo "Creating a kafka topic using kafka cli command"
docker exec -it $kafka_container bash -c "/bin/kafka-topics --bootstrap-server localhost:9092 --create --topic $task2_topic --partitions 3"

docker build -t $task2_application \
    --build-arg bootstrap_servers=$kafka_container:9092 \
    --build-arg topic=$task2_topic \
    . 
docker run \
    --net=$task2_network \
    -p 8000:$task2_application_port \
    --name $task2_application \
    $task2_application:latest 


