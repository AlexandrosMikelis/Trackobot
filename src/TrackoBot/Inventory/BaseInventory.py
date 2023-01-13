from abc import ABC, abstractmethod, abstractproperty

from TrackoBot.utilities import TObject

class BaseInventory(ABC):
    
    @property
    @abstractmethod
    def objects(self) -> list[TObject]:
        ...
        
    @property
    @abstractmethod
    def _workspace(self) -> None:
        ...
    
    @abstractmethod
    def addObject(self,object:TObject):
        pass
    
    @abstractmethod
    def removeObject(self, object:TObject):
        pass
    