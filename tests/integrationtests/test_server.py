from datetime import datetime, timedelta


def test_status_integration(test_client, connect_to_db):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=3)

    response = test_client.get(
        f"/status?start_time={start_time.isoformat()}&end_time={end_time.isoformat()}"
    )

    assert response.status_code == 200
    data = response.json()

    # Verify the counts match our test data
    assert data == {"0": 1, "1": 2, "2": 1}
