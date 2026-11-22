
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from main import app
from database import Base, get_db
from db_models import UserDB
from security import hash_password

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
        join_transaction_mode="create_savepoint"
    )

    db = TestingSessionLocal()

    admin = UserDB(
        username="nethara",
        email="admin@test.com",
        hashed_password=hash_password("AdminTest123!"),
        role="admin"
    )

    student = UserDB(
        username="student_account",
        email="student@test.com",
        hashed_password=hash_password("StudentTest123!"),
        role="student"
    )

    db.add_all([admin, student])
    db.commit()

    yield db

    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
