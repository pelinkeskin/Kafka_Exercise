# Project Overview
    This project is designed to scrape data from a specific website, process it into a JSON format, and then publish the resulting JSON data to a Kafka topic. The project consists of several modules:

* __main.py__: Orchestrates the data scraping and Kafka publishing process.
* __scrapper.py__: Contains the logic for scraping data from the target website.
* __kafka_producer.py__: Provides a class for producing messages to a Kafka cluster.
* __task2.sh__: Sets up a local Kafka environment using Docker.
* __Dockerfile__: Defines the Docker image used for the project.

# Dependencies
## Python libraries:
* confluent_kafka
* requests
* beautifulsoup4
* Flask
* gunicorn
## Docker

# Project Structure
```
project_directory/
├── main.py
├── task2.sh
├── Dockerfile
├── scrapper/
│   └── scrapper.py
└── kafka/
    └── kafka_producer.py
```

# Usage
## Prerequisites
* Docker installed and running
## Steps
### Clone the repository:
    git clone https://github.com/pelinkeskin/DBrain.git
### Bash
    sh task2.sh
    
# Explanation
## scrapper.py:
* Defines the Scrapper class to extract data from the target website.
* Provides methods for fetching content, extracting text and links, and creating JSON objects.
* To efficiently handle large web pages, the functionality should incorporate HTTP range requests to retrieve data in manageable chunks..
## kafka_producer.py:
* Implements a Kafka producer class with features like batching, delivery callbacks, and logging.
## main.py:
* Creates a Scrapper instance to scrape data from the website.
* Creates a kafka_producer instance to publish the scraped data to a Kafka topic.
* Flask API:  Defines a Flask app. to create an endpoint / that streams the contents of data.json.
## task2.sh:
* Sets up a local Kafka environment using Docker.
## Dockerfile:
* Defines the Docker image with necessary dependencies and environment variables.

# Potential Improvements
## Code-Specific Enhancements
### scrapper.py:
* Robustness can be improved by incorporating error handling mechanisms for network requests and parsing exceptions.
* Pagination functionality can be added to efficiently handle large product lists.
* Asynchronous request methods can be explored to optimize performance.
### kafka_producer.py:
* Publishing messages to Kafka synchronously can block the main thread, potentially causing the Flask application to hang. To mitigate this,   asynchronous Kafka message production can be implemented.
* Asynchronous waiting mechanisms could be considered as an alternative to the current sleep-based grace period implementation.
## Script-Level Considerations
### task2.sh:
* Instead of environment variables for container and network names, a configuration server could be employed for enhanced flexibility and maintainability.
## Clean-up

```
docker container rm -f task2_kafka task2_zookeeper task2_application
docker network rm -f task2_network 
```