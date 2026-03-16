import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities dict to its original state after each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

class TestGetActivities:
    def test_returns_200(self):
        response = client.get("/activities")
        assert response.status_code == 200

    def test_returns_all_activities(self):
        response = client.get("/activities")
        data = response.json()
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
        for name in expected_activities:
            assert name in data

    def test_activity_has_expected_fields(self):
        response = client.get("/activities")
        chess = response.json()["Chess Club"]
        assert "description" in chess
        assert "schedule" in chess
        assert "max_participants" in chess
        assert "participants" in chess


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

class TestSignup:
    def test_signup_success(self):
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"},
        )
        assert response.status_code == 200
        assert "newstudent@mergington.edu" in response.json()["message"]

    def test_signup_adds_participant(self):
        email = "newstudent@mergington.edu"
        client.post("/activities/Chess Club/signup", params={"email": email})
        assert email in app_module.activities["Chess Club"]["participants"]

    def test_signup_already_registered_returns_400(self):
        email = "michael@mergington.edu"  # already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email},
        )
        assert response.status_code == 400
        assert "Already signed up" in response.json()["detail"]

    def test_signup_unknown_activity_returns_404(self):
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "someone@mergington.edu"},
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/participants
# ---------------------------------------------------------------------------

class TestUnregister:
    def test_unregister_success(self):
        email = "michael@mergington.edu"  # existing participant in Chess Club
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": email},
        )
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_unregister_removes_participant(self):
        email = "michael@mergington.edu"
        client.delete("/activities/Chess Club/participants", params={"email": email})
        assert email not in app_module.activities["Chess Club"]["participants"]

    def test_unregister_unknown_activity_returns_404(self):
        response = client.delete(
            "/activities/Nonexistent Club/participants",
            params={"email": "someone@mergington.edu"},
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_participant_not_found_returns_404(self):
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "notamember@mergington.edu"},
        )
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
