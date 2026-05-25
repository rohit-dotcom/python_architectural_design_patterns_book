import requests
import pytest


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocations(add_stock):
    sku,other_sku=random_sku(),random_sku("other")

    early_batch=random_batchref(1)
    later_batch=random_batchref(2)
    other_batch=random_batchref(3)

    add_stock([
        Batch(early_batch,sku=sku,qty=100,eta="2026-05-25")
        Batch(later_batch,sku=sku,qty=100,eta="2026-05-26")
        Batch(other_batch,sku=other_sku,qty=100,eta="2026-05-25")
    ])
    url=config.get_api_url()

    order={"order_id":random_orderid(),"sku":sku,"qty":2,}

    r=requests.post(f"{url}/allocate",json-order)

    assert r.status_code==201
    assert r.json()['batchref']==201