import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


# Store the initial state of activities
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer team practices and matches",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, drills, and intramural tournaments",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "mason@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater production, acting workshops, and stagecraft",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debating, public speaking, and argumentation skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["logan@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, guest lectures, and science fairs",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "elijah@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test to ensure test isolation"""
    activities.clear()
    for activity_name, activity_data in INITIAL_ACTIVITIES.items():
        activities[activity_name] = copy.deepcopy(activity_data)
    yield
    # Cleanup after test if needed
    activities.clear()
    for activity_name, activity_data in INITIAL_ACTIVITIES.items():
        activities[activity_name] = copy.deepcopy(activity_data)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)
