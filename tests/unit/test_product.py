import pytest
from allocations.domain.model import Batch,Orderline,Product
from datetime import date
import allocations.domain.events as events

today=date.today


def test_records_out_of_stock_event_if_cannot_allocate():
    batch=Batch('batch1','WAVY-DESK',10,eta=today)
    line=Orderline('order1','WAVY-DESK',10)
    product=Product('WAVY-DES',[batch])

    product.allocate(line)

    line2=Orderline('order2','WAVY-DESK',10)

    allocation=product.allocate(line2)

    assert product.events[-1]==events.OutOfStock(sku='WAVY-CHAIR')
    assert allocation==None
    