import asyncio

import uvicorn
import json
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Depends
from pymongo import MongoClient
from pymongo.collection import Collection

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from constants import (
    RABBITMQ_HOST,
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    PUBLISH_TOPIC,
    RABBITMQ_SERVER_PORT,
)


def get_collection():
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection


def process_and_store_status():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(RABBITMQ_HOST, RABBITMQ_SERVER_PORT)

    def on_message_print(client, data, message):
        payload = json.loads(message.payload.decode())
        payload["created_at"] = datetime.now()
        collection = get_collection()
        collection.insert_one(payload)

    # SUBSCRIBE TO TOPIC
    subscribe.callback(on_message_print, PUBLISH_TOPIC)


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, process_and_store_status)
    yield


app = FastAPI(title="Status Logger", lifespan=lifespan)


@app.get("/status")
async def count_status(
    start_time: Optional[datetime] = Query(description="Start time in ISO format"),
    end_time: Optional[datetime] = Query(description="End time in ISO format"),
    collection: Collection = Depends(get_collection),
):
    pipeline = collection.aggregate(
        [
            {"$match": {"created_at": {"$gte": start_time, "$lt": end_time}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        ]
    )
    status_counts = {doc["_id"]: doc["count"] for doc in list(pipeline)}
    return status_counts


if __name__ == "__main__":
    uvicorn.run("__main__:app", port=8000, host="0.0.0.0", reload=True)
