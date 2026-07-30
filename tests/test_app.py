import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_state))


def test_root_redirects_to_the_static_homepage():
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_the_activity_catalog():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_a_participant():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_unregister_participant_removes_the_email():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"].startswith("Unregistered")
