import src.app as app_module


def test_signup_success(client):
    # Arrange
    email = "newstudent@mergington.edu"
    endpoint = "/activities/Chess Club/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"
    endpoint = "/activities/Chess Club/signup"

    # Act
    client.post(endpoint, params={"email": email})

    # Assert
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_already_registered_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"
    endpoint = "/activities/Chess Club/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "Already signed up" in response.json()["detail"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    endpoint = "/activities/Nonexistent Club/signup"
    email = "someone@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_missing_email_returns_422(client):
    # Arrange
    endpoint = "/activities/Chess Club/signup"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422
