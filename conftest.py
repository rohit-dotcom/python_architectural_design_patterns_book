import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,clear_mappers
import orm

@pytest.fixture
def in_memory_db():
    engine=create_engine('sqlite:///:memory:')
    orm.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session(in_memory_db):
    orm.start_mapper()
    db_session=sessionmaker(bind=in_memory_db)
    yield db_session()
    clear_mappers()