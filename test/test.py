from fastapi.testclient import TestClient

from app.main import app, students


client = TestClient(app)


# Clear database before each test
def setup_function():
    students.clear()


# -------------------------
# POST Tests
# -------------------------

def test_create_student_success():

    response = client.post(
        "/students",
        json={
            "id": 1,
            "name": "Shajid",
            "department": "CSE",
            "semester": 6,
            "cgpa": 3.75
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Shajid"


def test_create_duplicate_student():

    student = {
        "id": 1,
        "name": "Shajid",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.75
    }

    client.post("/students", json=student)

    response = client.post("/students", json=student)

    assert response.status_code == 400


# -------------------------
# GET Tests
# -------------------------

def test_get_all_students():

    client.post(
        "/students",
        json={
            "id": 1,
            "name": "Shajid",
            "department": "CSE",
            "semester": 6,
            "cgpa": 3.75
        }
    )

    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_student_success():

    client.post(
        "/students",
        json={
            "id": 1,
            "name": "Shajid",
            "department": "CSE",
            "semester": 6,
            "cgpa": 3.75
        }
    )

    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_student_not_found():

    response = client.get("/students/999")

    assert response.status_code == 404


# -------------------------
# PUT Tests
# -------------------------

def test_update_student_success():

    client.post(
        "/students",
        json={
            "id": 1,
            "name": "Shajid",
            "department": "CSE",
            "semester": 6,
            "cgpa": 3.50
        }
    )

    response = client.put(
        "/students/1",
        json={
            "id": 1,
            "name": "Shajid Updated",
            "department": "CSE",
            "semester": 7,
            "cgpa": 3.90
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Shajid Updated"
    assert response.json()["semester"] == 7


def test_update_student_not_found():

    response = client.put(
        "/students/999",
        json={
            "id": 999,
            "name": "Unknown",
            "department": "CSE",
            "semester": 5,
            "cgpa": 3.00
        }
    )

    assert response.status_code == 404


# -------------------------
# DELETE Tests
# -------------------------

def test_delete_student_success():

    client.post(
        "/students",
        json={
            "id": 1,
            "name": "Shajid",
            "department": "CSE",
            "semester": 6,
            "cgpa": 3.75
        }
    )

    response = client.delete("/students/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Student deleted successfully"


def test_delete_student_not_found():

    response = client.delete("/students/999")

    assert response.status_code == 404


# -------------------------
# Invalid Data Tests
# -------------------------

def test_invalid_cgpa():

    response = client.post(
        "/students",
        json={
            "id": 2,
            "name": "Test Student",
            "department": "CSE",
            "semester": 5,
            "cgpa": 5.0
        }
    )

    assert response.status_code == 422


def test_invalid_semester():

    response = client.post(
        "/students",
        json={
            "id": 3,
            "name": "Test Student",
            "department": "CSE",
            "semester": 15,
            "cgpa": 3.50
        }
    )

    assert response.status_code == 422
