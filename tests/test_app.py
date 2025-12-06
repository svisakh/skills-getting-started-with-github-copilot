"""Tests for the Mergington High School API"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


def test_root_redirect(client):
    """Test that root redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_get_activities_has_participants(client):
    """Test that activities include participants"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)
    assert len(data["Chess Club"]["participants"]) > 0


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    assert "newstudent@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonExistent%20Club/signup?email=student@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_participant(client):
    """Test unregistering a participant from an activity"""
    # First, add a participant
    client.post("/activities/Basketball%20Club/signup?email=teststudent@mergington.edu")
    
    # Then remove them
    response = client.delete("/activities/Basketball%20Club/unregister?email=teststudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    assert "teststudent@mergington.edu" not in activities_response.json()["Basketball Club"]["participants"]


def test_unregister_nonexistent_participant(client):
    """Test unregistering a participant who doesn't exist"""
    response = client.delete("/activities/Art%20Club/unregister?email=doesnotexist@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    response = client.delete("/activities/Fake%20Club/unregister?email=student@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_multiple_signups(client):
    """Test signing up multiple participants"""
    activity = "Drama Club"
    initial_count = len(client.get("/activities").json()[activity]["participants"])
    
    # Sign up two students
    client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=student1@test.edu")
    client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=student2@test.edu")
    
    # Verify both were added
    updated_activities = client.get("/activities").json()
    new_count = len(updated_activities[activity]["participants"])
    assert new_count == initial_count + 2
    assert "student1@test.edu" in updated_activities[activity]["participants"]
    assert "student2@test.edu" in updated_activities[activity]["participants"]
