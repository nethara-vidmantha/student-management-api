import pytest
import database
from security import create_access_token
from dependencies import get_app_info, get_student_not_found

def test_addition():
    result = 10 + 20

    assert result == 30

def test_subtraction():
    result = 10 - 5

    assert result == 5

def calculate_average(mark1, mark2):
    return (mark1 + mark2) / 2




@pytest.mark.parametrize(
    "mark1, mark2, expected",
    [
        (80, 90, 85),
        (60, 70, 65),
        (40, 50, 45),
        (100, 100, 100)
    ]
)
def test_calculate_average(mark1, mark2, expected):
    result = calculate_average(mark1, mark2)

    assert result == expected

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Student Management API!"
    }

def test_invalid_login(client):
    response = client.post(
        "/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

def test_successful_login(client):
    response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_students_with_token(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/students",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_get_students_without_token(client):
    response = client.get("/students")

    assert response.status_code == 401

def test_student_cannot_create_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "student_account",
            "password": "StudentTest123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "age": 22,
            "email": "test@example.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

def test_admin_can_create_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/students",
        json={
            "name": "Pytest Student",
            "age": 22,
            "email": "pytest@example.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

def test_create_student_invalid_age(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "age": 10,
            "email": "test@example.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422

def test_create_student_invalid_name(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/students",
        json={
            "name": "A",
            "age": 22,
            "email": "test@example.com"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422


def test_get_single_student(client):
    # Login as admin
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    # Create a student
    create_response = client.post(
        "/students",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    student_id = create_response.json()["id"]

    # Get that student
    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "John"


def test_get_nonexistent_student(client):
    response = client.get("/students/9999")

    assert response.status_code == 404


def test_patch_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/students",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    student_id = create_response.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={"name": "John Updated"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "John Updated"
    assert response.json()["age"] == 22
    assert response.json()["email"] == "john@example.com"


def test_put_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/students",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    student_id = create_response.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "Peter",
            "age": 25,
            "email": "peter@example.com"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Peter"
    assert response.json()["age"] == 25
    assert response.json()["email"] == "peter@example.com"


def test_delete_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/students",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    student_id = create_response.json()["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify that the student was deleted
    get_response = client.get(f"/students/{student_id}")

    assert get_response.status_code == 404


def test_filter_students(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create two students
    client.post(
        "/students",
        json={"name": "John", "age": 18, "email": "john@example.com"},
        headers=headers
    )

    client.post(
        "/students",
        json={"name": "Peter", "age": 25, "email": "peter@example.com"},
        headers=headers
    )

    response = client.get("/students/filter?min_age=20")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Peter"


def test_sort_students(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create students in an unsorted order
    client.post(
        "/students",
        json={"name": "John", "age": 25, "email": "john@example.com"},
        headers=headers
    )

    client.post(
        "/students",
        json={"name": "Peter", "age": 18, "email": "peter@example.com"},
        headers=headers
    )

    client.post(
        "/students",
        json={"name": "David", "age": 22, "email": "david@example.com"},
        headers=headers
    )

    response = client.get("/students/sort")

    ages = [student["age"] for student in response.json()]

    assert response.status_code == 200
    assert ages == [18, 22, 25]


def test_student_pagination(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create three students
    for name, age in [
        ("John", 20),
        ("Peter", 22),
        ("David", 24)
    ]:
        client.post(
            "/students",
            json={
                "name": name,
                "age": age,
                "email": f"{name.lower()}@example.com"
            },
            headers=headers
        )

    response = client.get(
        "/students/pagination?page=1&limit=2"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_invalid_pagination_limit(client):
    response = client.get(
        "/students/pagination?page=1&limit=150"
    )

    assert response.status_code == 422


def test_limited_students(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for name, age in [
        ("John", 20),
        ("Peter", 22),
        ("David", 24)
    ]:
        client.post(
            "/students",
            json={
                "name": name,
                "age": age,
                "email": f"{name.lower()}@example.com"
            },
            headers=headers
        )

    response = client.get("/students/limited")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_offset_students(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for name, age in [
        ("John", 20),
        ("Peter", 22),
        ("David", 24),
        ("Alex", 26)
    ]:
        client.post(
            "/students",
            json={
                "name": name,
                "age": age,
                "email": f"{name.lower()}@example.com"
            },
            headers=headers
        )

    response = client.get("/students/offset")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_students_with_owners(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/students",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        },
        headers=headers
    )

    response = client.get("/students-with-owners")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["student_name"] == "John"
    assert response.json()[0]["username"] == "nethara"


def test_patch_nonexistent_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.patch(
        "/students/9999",
        json={"name": "Updated Name"},
        headers=headers
    )

    assert response.status_code == 404


def test_put_nonexistent_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(
        "/students/9999",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        },
        headers=headers
    )

    assert response.status_code == 404

def test_delete_nonexistent_student(client):
    login_response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "AdminTest123!"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(
        "/students/9999",
        headers=headers
    )

    assert response.status_code == 404

def test_create_student_without_token(client):
    response = client.post(
        "/students",
        json={
            "name": "John",
            "age": 22,
            "email": "john@example.com"
        }
    )

    assert response.status_code == 401

def test_patch_student_without_token(client):
    response = client.patch(
        "/students/1",
        json={"name": "Updated Name"}
    )

    assert response.status_code == 401

def test_delete_student_without_token(client):
    response = client.delete("/students/1")

    assert response.status_code == 401

def test_successful_registration(client):
    response = client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewUser123!"
        }
    )

    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

def test_duplicate_username_registration(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "NewUser123!"
    }

    client.post("/register", json=user_data)

    response = client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "another@example.com",
            "password": "Another123!"
        }
    )

    assert response.status_code == 400

def test_registration_short_password(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 422

def test_duplicate_email_registration(client):
    client.post(
        "/register",
        json={
            "username": "userone",
            "email": "same@example.com",
            "password": "Password123!"
        }
    )

    response = client.post(
        "/register",
        json={
            "username": "usertwo",
            "email": "same@example.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 400


def test_registered_user_can_login(client):
    client.post(
        "/register",
        json={
            "username": "newloginuser",
            "email": "login@example.com",
            "password": "Password123!"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "newloginuser",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_registered_user_can_login(client):
    client.post(
        "/register",
        json={
            "username": "newloginuser",
            "email": "login@example.com",
            "password": "Password123!"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "newloginuser",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post(
        "/login",
        data={
            "username": "nethara",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_login_unknown_username(client):
    response = client.post(
        "/login",
        data={
            "username": "unknownuser",
            "password": "Password123!"
        }
    )

    assert response.status_code == 401


def test_registration_short_username(client):
    response = client.post(
        "/register",
        json={
            "username": "ab",
            "email": "short@example.com",
            "password": "Password123!"
        }
    )

    assert response.status_code == 422


def test_registration_invalid_email(client):
    response = client.post(
        "/register",
        json={
            "username": "emailuser",
            "email": "not-an-email",
            "password": "Password123!"
        }
    )

    assert response.status_code == 422


def test_get_db_closes_session(monkeypatch):
    class FakeSession:
        closed = False

        def close(self):
            self.closed = True

    fake_db = FakeSession()

    monkeypatch.setattr(
        database,
        "SessionLocal",
        lambda: fake_db
    )

    db_generator = database.get_db()

    db = next(db_generator)

    assert db is fake_db
    assert db.closed is False

    with pytest.raises(StopIteration):
        next(db_generator)

    assert db.closed is True


def test_invalid_token(client):
    headers = {
        "Authorization": "Bearer invalid_token_123"
    }

    response = client.get(
        "/students",
        headers=headers
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_token_without_username(client):
    token = create_access_token(data={})

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/students",
        headers=headers
    )

    assert response.status_code == 401


def test_token_for_nonexistent_user(client):
    token = create_access_token(
        data={"sub": "nonexistent_user"}
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/students",
        headers=headers
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_get_app_info():
    result = get_app_info()

    assert result["app_name"] == "Student Management API"
    assert result["version"] == "1.0.0"


def test_get_student_not_found():
    result = get_student_not_found()

    assert result["error"] == "Student not found"
    assert result["message"] == "The requested student does not exist."


def test_app_info_endpoint(client):
    response = client.get("/app-info")

    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Student Management API",
        "version": "1.0.0"
    }
