import requests
import pytest
import uuid
import config


def random_suffix():
    return uuid.uuid4().hex[:6]

def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"

def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"

def random_orderid(name=""):
    return f"order{name}-{random_suffix()}"

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocations():
    sku,other_sku=random_sku(),random_sku("other")

    early_batch=random_batchref(1)
    later_batch=random_batchref(2)
    other_batch=random_batchref(3)

    url=config.get_api_uri()

    batches=[{"batch_ref":early_batch,"sku":sku,"qty":100,"eta":"2026-05-25"},
    {"batch_ref":later_batch,"sku":sku,"qty":100,"eta":"2026-05-26"},
    {"batch_ref":other_batch,"sku":other_sku,"qty":100,"eta":"2026-05-25"}]

    for batch in batches:
        requests.post(f"{url}/add_batch",json=batch)

    order={"orderid":random_orderid(),"sku":sku,"qty":2}

    r=requests.post(f"{url}/allocate",json=order)

    assert r.status_code==201
    assert r.json()["batchref"]==early_batch

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_add_batch():
    batch=random_batchref()
    url=config.get_api_uri()
    sku=random_sku()

    batches=[{"batch_ref":batch,"sku":sku,"qty":10,"eta":"2026-05-25"}]

    for batch in batches:
        r=requests.post(f"{url}/add_batch",json=batch)
    assert r.status_code==201

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_400_out_of_stock_error():
    sku, small_batch, large_order=random_sku(),random_batchref(),random_orderid()
    url=config.get_api_uri()

    batches=[{"batch_ref":small_batch,"sku":sku,"qty":10,"eta":"2026-05-25"}]
    
    for batch in batches:
        requests.post(f"{url}/add_batch",json=batch)

    order={"orderid":large_order,"sku":sku,"qty":20}

    r=requests.post(f"{url}/allocate",json=order)

    assert r.status_code==400
    assert r.json()["message"]==f"Out of stock for {sku}"
