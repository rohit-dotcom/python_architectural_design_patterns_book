from adapters.repository import AbstractRepository
import domain.model as model
import services.services as services
import pytest




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
    batch=model.Batch('b1','s1',100,"2026-05-25")
    order=model.Orderline('o1','s1',10)
    repo=FakeRepository([batch])

    result=services.allocate(order,repo,FakeSession())

    assert result=="b1"

def test_invalid_sku():
    batch=model.Batch('b1','other_sku',100,"2026-05-25")
    order=model.Orderline('o1','s1',10)
    repo=FakeRepository([batch])

    
    with pytest.raises(services.InvalidSku,match='Invalid sku s1'):
        services.allocate(order,repo,FakeSession())

def test_commits():
    batch=model.Batch('b1','s1',100,"2026-05-25")
    order=model.Orderline('o1','s1',10)
    repo=FakeRepository([batch])
    session=FakeSession()

    result=services.allocate(order,repo,session)

    assert session.committed is True

def test_dellocates_restores_batch():
    batch=model.Batch('b1','s1',100,"2026-05-25")
    order=model.Orderline('o1','s1',10)
    repo=FakeRepository([batch])

    allocated_batch=services.allocate(order,repo,FakeSession())

    assert repo.get(allocated_batch).available_quantity==90

    allocated_batch=services.deallocate(order,allocated_batch,repo,FakeSession())

    assert repo.get(allocated_batch).available_quantity==100



