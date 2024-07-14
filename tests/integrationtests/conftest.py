import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from datetime import datetime, timedelta
from server import app, MONGO_URI, DB_NAME, COLLECTION_NAME


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def connect_to_db():
    # Connect to the test database
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Clear the collection before each test
    collection.delete_many({})

    # Insert test data
    now = datetime.now()
    test_data = [
        {"status": 0, "created_at": now - timedelta(hours=2)},
        {"status": 1, "created_at": now - timedelta(hours=1)},
        {"status": 1, "created_at": now - timedelta(minutes=30)},
        {"status": 2, "created_at": now},
    ]
    collection.insert_many(test_data)

    yield collection

    # Clean up after tests
    collection.delete_many({})
    client.close()
