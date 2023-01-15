from abc import ABC, abstractmethod, abstractproperty

from TrackoBot.utilities import TObject,Workspace
from TrackoBot.Inventory import Inventory


class BaseTrackobot(ABC):
    
    @abstractmethod
    def BarcodeDetection(self):
        pass
    
    @abstractmethod
    def TextRecognition(self):
        pass
    
    @abstractmethod
    def ExpDateRecongition(self):
        pass
    
    @abstractmethod
    def ObjTracker(self):
        pass