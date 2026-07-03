from domain import model

def insert_batch(session,orderid,sku,qty,eta):
    session.execute(
        F'INSERT INTO batches (orderid,sku,_purchased_quantity,eta) VALUES ("{orderid}","{sku}","{qty}","{eta}")'
    )

def test_unit_of_work_fetches_batch_then_allocates_to_it(session_factory):
    session=session_factory()
    insert_batch(session,'batch1','Hipster-workbench',100,eta=None)
    session.commit()

    uow=unit_of_work.SqlAlchemyUnitOfWork(session)
    with uow:
        batch=uow.batches.get(reference='batch1')
        
        line=model.Orderline('o1','Hipster-workbench',10)
        batch.allocate(line)
        uow.commit()

    batchref=get_allocated_batch(session,'o1','Hipster-workbench')

    assert batchref=='batch1'


        
