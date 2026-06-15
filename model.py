
from datetime import date
from dataclasses import dataclass
from typing import Optional,List



@dataclass(unsafe_hash=True)
class Orderline:
    orderid:str
    sku:str
    qty:int 


class OutOfStock(Exception):
    pass

class Batch():

    def __init__(self,batch_ref:str,sku:str,qty:int,eta:Optional[date]):
        self.batch_ref=batch_ref
        self.sku=sku
        self._purchased_quantity=qty
        self._allocations=set()
        self.eta=eta
    
    def __repr__(self):
        return f'<Batch {self.batch_ref}>'

    def allocate(self,order:Orderline):
        if self.can_allocate(order):
            self._allocations.add(order)

    def can_allocate(self,line:Orderline)->bool:
        return self.sku==line.sku and self.available_quantity>=line.qty
    
    def deallocate(self,order):
        if order in self._allocations:
            self._allocations.remove(order)


    
    @property
    def allocated_quantity(self,):
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self,):
        return self._purchased_quantity-self.allocated_quantity
    
    def __eq__(self,other):
        
        if not isinstance(other,Batch):
            return False
        return self.batch_ref==other.batch_ref

    def __hash__(self):

        return hash(self.batch_refs)
    
    def __gt__(self,other):
        if self.eta is None:
            return False
        if other.eta is None:
            return False
        else:
            return self.eta>other.eta

    def __lt__(self,other):
        if self.eta is None:
            return False
        if other.eta is None:
            return False
        else:
            return self.eta<other.eta

def allocate(line:Orderline,batches:List[Batch]):

    try:
        earliest_batch=next(b for b in sorted(batches) if b.can_allocate(line))
        earliest_batch.allocate(line)
        return earliest_batch.batch_ref
    except StopIteration:
        raise OutOfStock(f'Out of stock for {line.sku}')
