import src.app as app_module


def test_unregister_success(client):
    # Arrange
    email = "michael@mergington.edu"
    endpoint = "/activities/Chess Club/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    endpoint = "/activities/Chess Club/participants"

    # Act
    client.delete(endpoint, params={"email": email})

    # Assert
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    endpoint = "/activities/Nonexistent Club/participants"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_not_found_returns_404(client):
    # Arrange
    endpoint = "/activities/Chess Club/participants"
    email = "notamember@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_missing_email_returns_422(client):
    # Arrange
    endpoint = "/activities/Chess Club/participants"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422
