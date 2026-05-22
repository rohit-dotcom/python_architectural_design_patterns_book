from abc import ABC,abstractmethod
import model

def AbstractRepository(ABC):
    @abstractmethod
    def add(self,batch=model.Batch):
        pass

    @abstractmethod
    def get(self,reference)->model.Batch:
        pass

