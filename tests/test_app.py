from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_cannot_sign_up_same_student_twice():
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert second_response.status_code == 400
