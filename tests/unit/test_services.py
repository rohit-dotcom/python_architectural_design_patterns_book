from adapters.repository import AbstractRepository
import services.services as services
import pytest
from datetime import date,timedelta
from domain import model




class FakeRepository(AbstractRepository):
    def __init__(self,batches):
        self._batches=set(batches)

    def add(self,batch):
        self._batches.add(batch)


    def get(self,reference)->model.Batch:
        return next(b for b in self._batches if b.batch_ref==reference)
    
    def list(self):
        return list(self._batches)


class FakeSession():
    committed=False

    def commit(self):
        self.committed=True

def test_returns_allocations():
    repo=FakeRepository([])
    session=FakeSession()
    services.add_batch('b1','s1',100,"2026-05-25",repo,session)   

    result=services.allocate('o1','s1',10,repo,FakeSession())

    assert result=="b1"

def test_invalid_sku():
    repo=FakeRepository([])
    session=FakeSession()
    services.add_batch('b1','s1',100,"2026-05-25",repo,session)

    
    with pytest.raises(services.InvalidSku,match='Invalid sku different'):
        services.allocate('o1','different',10,repo,session)


def test_commits():
    repo=FakeRepository([])
    session=FakeSession()
    services.add_batch('b1','s1',100,"2026-05-25",repo,session)

    services.allocate('o1','s1',10,repo,session)

    assert session.committed is True

def test_dellocates_restores_batch():
    repo=FakeRepository([])
    session=FakeSession()
    services.add_batch('b1','s1',100,"2026-05-25",repo,session)

    allocated_batch=services.allocate('o1','s1',10,repo,session)

    assert repo.get(allocated_batch).available_quantity==90

    services.deallocate('o1','s1',10,repo,session)

    assert repo.get(allocated_batch).available_quantity==100

def test_deallocate_the_unallocated_batch():
    repo=FakeRepository([])
    session=FakeSession()
    services.add_batch('b1','s1',100,"2026-05-25",repo,session)

    services.allocate('o1','s1',10,repo,session)
    batch_added=repo.get("b1")

    assert batch_added.available_quantity==90

    services.deallocate('o1','s1',10,repo,session)

    assert batch_added.available_quantity==100

    services.deallocate('o1','s1',10,repo,session)

    assert batch_added.available_quantity==100

def test_prefers_current_stock_batches_to_in_transit():
    repo=FakeRepository([])
    session=FakeSession()
    services.add_batch('batch-002','foot-pedestal',100,None,repo,session)
    services.add_batch('batch-003','foot-pedestal',100,date.today()+timedelta(days=1),repo,session)

    services.allocate('order-122','foot-pedestal',10,repo,FakeSession())
    assert repo.get('batch-002').available_quantity==90
