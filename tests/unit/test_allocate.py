from domain.model import Batch, Orderline,allocate,OutOfStock
from datetime import date,timedelta
import pytest


def test_allocating_to_a_batch_reduces_the_availabel_quantity():
    batch=Batch('batch-001',"SMALL-CHAIR", qty=20,eta=date.today())
    line=Orderline('order-001',"SMALL-CHAIR",qty=2)

    batch.allocate(line)

    assert batch.available_quantity==18

def make_batch_and_line(sku,batch_qty,line_qty):
    return Batch('batch-001',sku,qty=batch_qty,eta=date.today()),Orderline('order-001',sku,qty=line_qty)

def test_can_allocate_if_batch_qty_more_than_order_qty():
    large_batch,small_line=make_batch_and_line('small_chair',20,3)

    assert large_batch.can_allocate(small_line)

def test_can_allocate_if_batch_qty_equal_to_order_qty():
    equal_batch,equal_line=make_batch_and_line('small_chair',20,20)

    assert equal_batch.can_allocate(equal_line)


def test_cannot_allocate_if_batch_qty_smaller_to_order_qty():
    small_batch,large_line=make_batch_and_line('small_chair',10,20)

    assert small_batch.can_allocate(large_line) is False


def test_cannot_allocate_if_batch_sku_not_equal_to_batch():
    batch=Batch('batch-001',"LARGE-CHAIR", qty=20,eta=date.today())
    line=Orderline('order-001',"SMALL-CHAIR",qty=2)


    assert batch.can_allocate(line) is False

def test_can_only_deallocate_allocated_lines():
    batch,unallocated_line=make_batch_and_line("superman-cape",20,4    )
    
    batch.deallocate(unallocated_line)

    assert batch.available_quantity==20

def test_allocations_are_idempotent():
    batch,unallocated_line=make_batch_and_line("superman-cape",20,4    )
    
    batch.allocate(unallocated_line)
    batch.allocate(unallocated_line)

    assert batch.available_quantity==16

def test_prefers_current_stock_batches_to_in_transit():
    in_stock_batch=Batch('batch-002','foot-pedestal',qty=100,eta=None)
    in_shipment_batch=Batch('batch-003','foot-pedestal',qty=100,eta=date.today()+timedelta(days=1))
    line=Orderline('order-122','foot-pedestal',qty=10)

    allocate(line,[in_stock_batch,in_shipment_batch])
    assert in_stock_batch.available_quantity==90

def test_prefers_current_earliest_batches_to_in_transit():
    in_later=Batch('batch-002','foot-pedestal',qty=100,eta=date.today()+timedelta(days=3))
    in_today=Batch('batch-002','foot-pedestal',qty=100,eta=date.today()+timedelta(days=1))
    in_tomorrow=Batch('batch-003','foot-pedestal',qty=100,eta=date.today()+timedelta(days=2))
    line=Orderline('order-122','foot-pedestal',qty=10)

    allocate(line,[in_later,in_today,in_tomorrow])

    assert in_today.available_quantity==90

def test_returns_allocated_batch_reference():
    in_later=Batch('batch-002','foot-pedestal',qty=100,eta=date.today()+timedelta(days=3))
    in_today=Batch('batch-002','foot-pedestal',qty=100,eta=date.today()+timedelta(days=1))
    in_tomorrow=Batch('batch-003','foot-pedestal',qty=100,eta=date.today()+timedelta(days=2))
    line=Orderline('order-122','foot-pedestal',qty=10)

    allocated_batch_ref=allocate(line,[in_later,in_today,in_tomorrow])

    assert in_today.batch_ref==allocated_batch_ref  


def test_raises_out_of_stock_exception_incase_out_of_stock():
    in_today=Batch('batch-002','foot-pedestal',qty=100,eta=date.today()+timedelta(days=1))
    line=Orderline('order-122','foot-pedestal',qty=100)

    allocate(line,[in_today])

    with pytest.raises(OutOfStock,match='foot-pedestal'):
        allocate(Orderline('order-123','foot-pedestal',qty=10),[in_today])
