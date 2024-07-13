import datetime


def test_status_route(client, mock_mongo_aggregate):
    params = {
        "start_time": datetime.datetime.now(),
        "end_time": datetime.datetime.now(),
    }
    response = client.get("/status", params=params)

    assert response.json() == {"0": 2, "1": 8, "2": 1}
    assert response.status_code == 200
