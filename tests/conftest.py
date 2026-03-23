import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def random_email():
    import random
    return f"tester_{random.randint(1000, 99999)}@example.com"
