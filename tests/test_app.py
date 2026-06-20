import pytest

from src.app import activities


# Tests follow the Arrange-Act-Assert (AAA) pattern and use the
# `client` and `reset_activities` fixtures from tests/conftest.py


def test_get_activities(client, reset_activities):
    # Arrange: none (activities is in its initial state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_adds_participant(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "newparticipant@example.com"
    before_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json().get("message") == f"Signed up {email} for {activity_name}"
    assert len(activities[activity_name]["participants"]) == len(before_participants) + 1


def test_signup_duplicate_returns_400(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    # Use an email already in the initial participants list
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json().get("detail") is not None


def test_unregister_removes_participant(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json().get("message") == f"Unregistered {email} from {activity_name}"


def test_nonexistent_activity_returns_404(client, reset_activities):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "someone@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json().get("detail") == "Activity not found"
