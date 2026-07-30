from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_the_email_from_activity():
    response = client.delete(
        "/activities/Chess%20Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"].startswith("Unregistered")


def test_unregister_participant_returns_404_for_missing_participant():
    response = client.delete(
        "/activities/Chess%20Club/participants/not-a-student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
