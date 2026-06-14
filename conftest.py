import time
from pathlib import Path
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
import pytest
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,clear_mappers
from orm import metadata,start_mapper
import config
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

def wait_for_postgres_to_come_up(engine):
    deadline=time.time()+5
    while time.time()<deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up!")

def wait_for_webapp_to_come_up():
    deadline=time.time()+5
    url=config.get_api_uri()
    while time.time()<deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("Webapp never came up!!")


@pytest.fixture(scope="session")
def postgres_db():
    engine=create_engine(config.get_postgres_url())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    return engine

@pytest.fixture
def postgres_session(postgres_db):
    start_mapper()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()

@pytest.fixture
def add_stock(postgres_session):
    batches_added=set()
    skus_added=set()

    def _add_stock(lines):
        for ref,sku,qty,eta in lines:
            postgres_session.execute(text(f"""
                INSERT INTO batches (batch_ref,sku,_purchased_quantity,eta)
                VALUES ('{ref}','{sku}','{qty}','{eta}')"""
                
            ))
            
            [[batch_id]]=postgres_session.execute(text(f"""
            SELECT id FROM batches WHERE batch_ref='{ref}' and sku='{sku}'""") )

            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()
    
    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(text(f"""
            DELETE FROM allocations WHERE batch_id='{batch_id}' """

        ))
        postgres_session.execute(text(f"""
            DELETE FROM batches WHERE batch_ref='{batch_id}' """

        ))

    for sku in skus_added:
        postgres_session.execute(text(f"""
            DELETE FROM order_lines WHERE sku='{sku}' """

        ))
        postgres_session.commit()

@pytest.fixture
def restart_api():
    (Path(__file__).parent/"flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()










