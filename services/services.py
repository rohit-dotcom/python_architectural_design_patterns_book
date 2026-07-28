from adapters.repository import AbstractRepository
import allocations.domain.model as model
from typing import Optional
from datetime import date



class InvalidSku(Exception):
    pass

def is_valid_sku(sku,batches):
    return sku in {b.sku for b in batches}

def add_batch(batch_ref:str,sku:str,qty:int,eta:Optional[date],repo:AbstractRepository,session)->None:
    batch=model.Batch(batch_ref,sku,qty,eta)
    repo.add(batch)
    session.commit()


def allocate(order_id:str,sku:str,qty:int,uow:unit_of_work.AbstractUnitOfWork)->str:

    line=model.Orderline(order_id,sku,qty)
    with uow:
        batches=uow.batches.list()
        if not is_valid_sku(line.sku,batches):
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref=model.allocate(line,batches)
        uow.commit()
    return batchref

def deallocate(order_id:str,sku:str,qty:int,uow:unit_of_work.AbstractUnitOfWork)->str:
    line=model.Orderline(order_id,sku,qty)
    batches=uow.batches.list()
    #check if allocated
    with uow:
        if not is_valid_sku(line.sku,batches):
            raise InvalidSku(f"Invalid sku {line.sku}")
        sku_batches=[b for b in batches if b.sku==line.sku]
        for b in sku_batches:
            b.deallocate(line)
            uow.commit()

