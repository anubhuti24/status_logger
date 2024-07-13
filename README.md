# Status Logger Using RabbitMQ

Client-server script in Python that handles MQTT messages via RabbitMQ

## Requirements

- MongoDB: [Installation Guide](https://www.mongodb.com/docs/manual/installation/)
- RabbitMQ: [Installation Guide](https://www.rabbitmq.com/docs/download)
- Python 3.12.1
- Poetry: [Installation Guide](https://python-poetry.org/docs/#installation)

## Installation

Install using poetry:
```sh
poetry shell
poetry install --no-root
```

## Start rabbitmq-server
Start the RabbitMQ server in the background.
```sh
sudo systemctl start rabbitmq-server
```

## Publish messages 
Run client.py file which will emit MQTT messages via RabbitMQ.

```sh
python3 client.py
```

## Start the application server
This is a fastapi application which will process the incoming MQTT messages as a sub-process, store the processed messages in the database (i.e. MongoDB).
An endpoint is provided to return the count of each status within the specified time range using MongoDB's aggregate pipeline.

This endpoint will take start and end time as Query Parameters.
```sh
python3 server.py
```

## Run unit test
```sh
pytest -v
```