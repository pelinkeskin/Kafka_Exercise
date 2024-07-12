# Project Overview
	This repository contains two independent projects:

* __task1:__ Sets up a local Kafka environment using Docker for testing and development purposes.
* __task2:__ Scrapes data from a website, processes it into JSON format, and publishes it to a Kafka topic.

## Project Structure
```python
project_directory/
├── task1/
│   └── setup_kafka.sh
└── task2/
    ├── main.py
    ├── scrapper.py
    ├── kafka_producer.py
    ├── task2.sh
    ├── Dockerfile
```

## Getting Started
### [Task 1: Local Kafka Environment Setup](task1/)
* Navigate to the task1 directory.
* Refer to the [README.md](task1/README.md) file in that directory for detailed instructions on setting up the Kafka environment.
### [Task 2: Web Scraping and Kafka Producer](task2/)
* Navigate to the task2 directory.
* Refer to the [README.md](task2/README.md) file in that directory for detailed instructions on running the project, dependencies, usage, and potential improvements.
### Additional Notes
* The projects are designed to be independent and can be used separately.
* The provided README.md files in each project directory contain specific instructions and details.
* We preferred Confluent distribution of Apache Kafka because it is the closest version to a real production environment.
* We didn't use Docker Compose because the task suggest us to use regular Docker, whereas same functionality can be achieve with Docker Compose.
