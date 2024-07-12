#!/bin/bash

# Define container and network names for consistency
kafka_container=task1_kafka
zookeeper_container=task1_zookeeper
task1_network=task1_network

# Create an isolated Docker network for the Kafka environment
docker network create task1_network

# Start Zookeeper container within the created network
docker run \
    --name $zookeeper_container \
    --net=$task1_network \
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
    --net=$task1_network \
    --name $kafka_container \
    --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
    --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    --env KAFKA_ZOOKEEPER_CONNECT=$zookeeper_container:2181 \
    -d confluentinc/cp-kafka:7.5.5 

# Wait for Kafka to be ready
sleep 5

# Create a kafka topic with 3 partitions using kafka cli command
echo "Creating a kafka topic using kafka cli command"
docker exec -it $kafka_container bash -c "/bin/kafka-topics --bootstrap-server localhost:9092 --create --topic task1-topic --partitions 3"

# Send message to kafka topic using kafka cli command
echo "Sending message to kafka topic using kafka cli command"
docker exec -it $kafka_container bash -c  'cat <<< "1:task1_message" | /bin/kafka-console-producer --bootstrap-server localhost:9092 --topic task1-topic --property "parse.key=true" --property "key.separator=:"' 

# Listen messages produced on some topic using kafka cli command with 10 second timeout
echo "Listening messages produced on some topic using kafka cli command with 10 second timeout"
docker exec -it $kafka_container bash -c  'timeout 10 /bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic task1-topic --from-beginning --property "parse.key=true" --property "key.separator=:"'

# Clean up containers and network
echo "Cleaning up containers and network"
docker container rm -f $kafka_container $zookeeper_container
docker network rm -f $task1_network
