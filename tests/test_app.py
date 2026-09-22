from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: sign up the student
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert: signup succeeds
    assert signup_response.status_code == 200

    # Act: remove the student from the activity
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert: unregister succeeds and the email is removed from the list
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_cannot_sign_up_same_student_twice():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    # Act: register the student the first time
    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert: initial sign up succeeds
    assert first_response.status_code == 200

    # Act: register the same student again
    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert: duplicate registration is rejected
    assert second_response.status_code == 400
