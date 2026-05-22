import model
from sqlalchemy import text


# from orm import start_mapper

# def test_orm_mapping_can_load_lines(db_session):
#     start_mapper()


def test_orm_mapping_can_lOad_lines(db_session):
    db_session.execute(text('INSERT INTO order_lines (orderid, sku, qty) VALUES '
'("order1", "RED-CHAIR", 12),'
'("order1", "RED-TABLE", 13),'
'("order2", "BLUE-LIPSTICK", 14)')
)
    
    expected= [model.Orderline("order1","RED-CHAIR",12),
                model.Orderline("order1","RED-TABLE",13),
                model.Orderline("order2","BLUE-LIPSTICK",14)]
    print(db_session.query(model.Orderline).all())
    assert db_session.query(model.Orderline).all()==expected

def test_orderline_mapper_can_save_lines(db_session):
    newline=model.Orderline('order2','Watch-Omega',10)
    db_session.add(newline)
    db_session.commit()

    rows=db_session.execute(text("SELECT orderid,sku,qty FROM 'order_lines'")).all()

    assert rows==[('order2','Watch-Omega',10)]
