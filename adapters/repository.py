from abc import ABC,abstractmethod
import domain.model as model

class AbstractRepository(ABC):
    @abstractmethod
    def add(self,batch=model.Batch):
        pass

    @abstractmethod
    def get(self,reference)->model.Batch:
        pass

class SQLAlchemyRepository(AbstractRepository):
    def __init__(self,session):
        self.session=session

    def add(self,batch):
        self.session.add(batch)

    def get(self,reference):
        return self.session.query(model.Batch).filter_by(batch_ref=reference).one()
    
    def list(self):
        return self.session.query(model.Batch).all()