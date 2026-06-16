import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to known state before each test"""
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        }
    })


class TestGetActivities:
    """Tests for retrieving activities"""

    def test_get_activities(self, client):
        # ARRANGE
        # Activities are loaded in the system via reset_activities fixture

        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert data["Chess Club"]["participants"] == ["michael@mergington.edu"]


class TestSignup:
    """Tests for signup functionality"""

    def test_signup_success(self, client):
        # ARRANGE
        email = "john@mergington.edu"
        activity = "Programming Class"

        # ACT
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 200
        assert f"Signed up {email} for {activity}" in response.json()["message"]
        
        # Verify participant was added
        response = client.get("/activities")
        assert email in response.json()["Programming Class"]["participants"]

    def test_signup_duplicate(self, client):
        # ARRANGE
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # ACT
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self, client):
        # ARRANGE
        email = "test@mergington.edu"
        activity = "Nonexistent Club"

        # ACT
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestRemoveParticipant:
    """Tests for participant removal functionality"""

    def test_remove_participant_success(self, client):
        # ARRANGE
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # ACT
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 200
        assert f"Removed {email} from {activity}" in response.json()["message"]
        
        # Verify participant was removed
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]

    def test_remove_nonexistent_participant(self, client):
        # ARRANGE
        email = "nothere@mergington.edu"
        activity = "Chess Club"

        # ACT
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_from_nonexistent_activity(self, client):
        # ARRANGE
        email = "someone@mergington.edu"
        activity = "Fake Club"

        # ACT
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
