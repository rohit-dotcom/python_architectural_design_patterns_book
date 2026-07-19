import pytest
from domain import model
from allocations.service_layer import unit_of_work
from sqlalchemy import text


def insert_batch(session, orderid, sku, qty, eta):
    session.execute(
        text(
            """
            INSERT INTO batches (batch_ref, sku, _purchased_quantity, eta)
            VALUES (:orderid, :sku, :qty, :eta)
            """
        ),
        {"orderid": orderid, "sku": sku, "qty": qty, "eta": eta},
    )

def get_allocated_batch(session,orderid,sku):
    [[orderlineid]]=session.execute(text(
    f'SELECT ID FROM order_lines WHERE orderid="{orderid}" AND  sku ="{sku}"'))

    [[batchref]]=session.execute(text(
    f'SELECT b.batch_ref FROM allocations JOIN batches as b on batch_id=b.id WHERE orderline_id="{orderlineid}"'))

    return batchref

def test_unit_of_work_fetches_batch_then_allocates_to_it(session_factory):
    session=session_factory()
    insert_batch(session,'batch1','Hipster-workbench',100,eta=None)
    session.commit()


    uow=unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch=uow.batches.get(reference="batch1")

        
        line=model.Orderline('o1','Hipster-workbench',10)
        batch.allocate(line)
        uow.commit()

    batchref=get_allocated_batch(session,'o1','Hipster-workbench')

    assert batchref=='batch1'

def test_rolls_back_uncommited_work_by_default(session_factory):
    uow=unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session,'batch1','Hipster-chair',100,eta=None)
    new_session=session_factory()
    rows=list(new_session.execute(text("SELECT * FROM batches")))
    assert rows==[]

def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass
    uow=unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session,'batch1','Hipster-chair',100,None)
            raise MyException
    new_session=session_factory()
    rows=list(new_session.execute(text('SELECT * FROM batches')))
    assert rows==[]

        
