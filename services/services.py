from adapters.repository import AbstractRepository
import domain.model as model


class InvalidSku(Exception):
    pass

def is_valid_sku(sku,batches):
    return sku in {b.sku for b in batches}

def allocate(line:model.Orderline,repo:AbstractRepository,session)->str:
    batches=repo.list()
    if not is_valid_sku(line.sku,batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref=model.allocate(line,batches)
    session.commit()
    return batchref

def deallocate(line:model.Orderline,repo:AbstractRepository,session)->str:
    batches=repo.list()
    #check if allocated
    if not is_valid_sku(line.sku,batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    sku_batches=[b for b in batches if b.sku==line.sku]
    for b in sku_batches:
        b.deallocate(line)
        session.commit()

