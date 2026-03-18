def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code in [302, 307]
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_200(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_expected_activities(client):
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Drama Society",
        "Math Olympiad",
        "Debate Club",
    ]

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_activity_has_expected_fields(client):
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    chess = response.json()["Chess Club"]

    # Assert
    for field_name in required_fields:
        assert field_name in chess
