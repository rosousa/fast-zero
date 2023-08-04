import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Base


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
