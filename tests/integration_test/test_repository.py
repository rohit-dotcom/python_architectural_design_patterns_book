from domain.model import Batch
import adapters.repository as repository
from sqlalchemy import text


def test_repository_can_save_a_batch(db_session):
    batch=Batch('batch1','Watch-Omega',10,eta=None)

    repo=repository.SQLAlchemyRepository(db_session)
    repo.add(batch)
    db_session.commit()

    rows=db_session.execute(text("SELECT batch_ref,sku,_purchased_quantity,eta from batches")).all()

    assert rows==[('batch1','Watch-Omega',10,None)]

def insert_order_lines(db_session):
    db_session.execute(text("INSERT INTO order_lines (orderid,sku,qty)"
             'VALUES ("order1","GENERIC-SOFA",12)')
    )
    [[orderline_id]]=db_session.execute(text(
        f"SELECT id FROM order_lines WHERE orderid='order1' AND sku='GENERIC-SOFA'"
    ))
    return orderline_id

def insert_batch(db_session,batch_id):
    db_session.execute(text(f"""INSERT INTO batches (batch_ref,sku,_purchased_quantity,eta)
             VALUES ("{batch_id}","GENERIC-SOFA",12,null)""")
    )
    [[batch_ref]]=db_session.execute(
        text(f"SELECT id FROM batches WHERE batch_ref='{batch_id}' AND sku='GENERIC-SOFA'")
    )
    return batch_ref

def insert_allocations(db_session,order_id,batch_ref):
    db_session.execute(text(f"""
        INSERT INTO allocations (orderline_id,batch_id) 
        VALUES ('{order_id}','{batch_ref}')"""))
        

def test_repository_can_retrieve_a_batch_with_allocatoins(db_session):
    orderline_id=insert_order_lines(db_session)
    batch_ref=insert_batch(db_session,"batch_1")
    insert_batch(db_session,"batch-2")
    insert_allocations(db_session,orderline_id,batch_ref)

    repo=repository.SQLAlchemyRepository(db_session)
    retrived_batch=repo.get("batch_1")
    expected=Batch("batch_1","GENERIC-SOFA",12,None)
    assert retrived_batch==expected
    assert retrived_batch.sku==expected.sku
    assert retrived_batch._purchased_quantity==expected._purchased_quantity
