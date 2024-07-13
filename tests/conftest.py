import pytest
from fastapi.testclient import TestClient

from server import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app=app)


@pytest.fixture
def mock_mongo_aggregate(mocker):
    mock = mocker.patch("pymongo.collection.Collection.aggregate")
    mock.return_value = [
        {"_id": 0, "count": 2},
        {"_id": 1, "count": 8},
        {"_id": 2, "count": 1},
    ]
