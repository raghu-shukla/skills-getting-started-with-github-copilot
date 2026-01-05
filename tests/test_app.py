from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # activities should include a known activity
    assert "Basketball Team" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "test_student@example.com"

    # Ensure email not already in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Soccer Team"
    email = "nonexistent@example.com"
    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in activity"
