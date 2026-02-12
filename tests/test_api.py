from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pytest
from unittest.mock import patch
import base64

# Override settings *before* importing app.main or app.database
from app.core.config import settings
TEST_DATABASE_URL = "sqlite:///./test.db"
settings.DATABASE_URL = TEST_DATABASE_URL

# Now import necessary components from the application
from app.api.v1.api import router as api_v1_router # Import the v1 router directly
from app.database import Base, get_db, get_engine, get_session_local

# Import models to ensure they are registered with Base.metadata.
# These imports must happen BEFORE Base.metadata.create_all() is called.
from app.models.document import Document
from app.models.user import User

# --- Test Database Setup ---
test_engine = get_engine(TEST_DATABASE_URL)
TestingSessionLocal = get_session_local(test_engine)

# Dependency to get the test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Fixtures ---
@pytest.fixture(name="db_session")
def db_session_fixture():
    # Create tables before each test
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal() # Create a session to yield
    try:
        yield db
    finally:
        db.close()
        # Drop tables after each test
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(name="fastapi_app")
def fastapi_app_fixture():
    # Create a new FastAPI app instance for testing
    test_app = FastAPI()
    test_app.include_router(api_v1_router, prefix="/api/v1")
    
    # Override get_db dependency for the test app
    test_app.dependency_overrides[get_db] = override_get_db
    return test_app

@pytest.fixture(name="client")
def client_fixture(fastapi_app: FastAPI, db_session): # Explicitly depend on db_session
    with TestClient(fastapi_app) as test_client:
        yield test_client

# --- Tests ---
@patch("app.api.v1.endpoints.health.redis.from_url")
def test_health_check(mock_redis_from_url, client):
    # Mock the Redis ping method
    mock_redis_from_url.return_value.ping.return_value = True

    response = client.get("/api/v1/health")
    if response.status_code != 200:
        print(f"Health check failed with status {response.status_code}: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "All services are healthy"}

@patch("app.worker.tasks.process_image_for_extraction.delay")
@patch("app.api.v1.endpoints.extraction.is_valid_image", return_value=True) # Corrected patch target
def test_upload_and_extract(
    mock_is_valid_image,
    mock_celery_delay,
    client,
):
    # Create a dummy image file for upload
    dummy_image_content = b"fake_image_data"
    files = {"file": ("test.jpg", dummy_image_content, "image/jpeg")}
    country_code = "FR"

    response = client.post(
        "/api/v1/upload-and-extract/",
        files=files,
        data={"country_code": country_code}
    )
    if response.status_code != 200:
        print(f"Upload and Extract failed with status {response.status_code}: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.jpg"
    assert data["status"] == "pending"
    assert "id" in data
    assert "upload_timestamp" in data

    # Verify that the Celery task was called
    mock_celery_delay.assert_called_once_with(
        data["id"],
        base64.b64encode(dummy_image_content).decode("utf-8"),
        country_code
    )

def test_get_extraction_task_status(client, db_session: Session):
    # First, create a dummy document in the database
    new_doc = Document(filename="test_doc.jpg", status="completed", owner_id=1, extracted_data={"field": "value"})
    db_session.add(new_doc)
    db_session.commit()
    db_session.refresh(new_doc)

    response = client.get(f"/api/v1/task-status/{new_doc.id}")
    assert response.status_code == 200
    assert response.json()["filename"] == "test_doc.jpg"
    assert response.json()["status"] == "completed"
    assert response.json()["extracted_data"] == {"field": "value"}
