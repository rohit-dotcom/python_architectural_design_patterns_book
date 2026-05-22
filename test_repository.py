from model import Batch

def test_repository_can_save_a_batch(db_session):
    batch=Batch('order=001','Watch-Omega',10,eta=None)

    repo=repository.SQLAlchemyRepository(db_session)
    repo.add(batch)
    repo.commit()

    rows=repo.execute("SELECT batch-ref,sku,_purchased_quantity,eta from batches")

    assert rows==[('order-001','Watch-Omega',10,None)]
