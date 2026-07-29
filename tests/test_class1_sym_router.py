from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_student_get_all():
    response = client.get("/student/getall")

    assert response.status_code == 200

    students = response.json()
    assert len(students) == 10
    assert students[0] == {"id": 1, "subject": "Python", "score": 100}

    allowed_subjects = {"Python", "Streamlit", "FastAPI"}
    for student in students:
        assert set(student) == {"id", "subject", "score"}
        assert isinstance(student["id"], int)
        assert student["subject"] in allowed_subjects
        assert isinstance(student["score"], int)
