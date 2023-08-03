import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fast_zero.models import Base


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield session()
    Base.metadata.drop_all(engine)
