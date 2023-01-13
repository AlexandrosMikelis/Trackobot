from .BaseInventory import BaseInventory
from TrackoBot.utilities import TObject, Workspace

class Inventory(BaseInventory):
    
    objects = []
    _workspace = None
    
    def __init__(self,workspace:Workspace):
        super().__init__() 
        Inventory._workspace = workspace
    
    def display(self):
        for obj in Inventory.objects:
            print(obj)
    
    def sortObjects(self, method:str):
        dublicate = False
        cleaned_inventory = [Inventory.objects[0]]
        for obj in Inventory.objects:
            for item in cleaned_inventory:
                if obj.name == item.name:
                    item.quantity += 1
                    dublicate=True
            if not dublicate:
                obj.quantity = 1
                cleaned_inventory.append(obj)
        
        return cleaned_inventory
                
    
    def setPriority(self, objects:list[TObject], priority_type:str):
        pass
    
    def isEmpty(self):
        return False if Inventory.objects else True
    
    def contains(self,object: TObject):
        if object in Inventory.objects : return True
        else: return False
        
    def increaseQuantity(self, barcode):
        for obj in Inventory.objects:
            if obj.barcode == barcode:
                obj.quantity +=1
                break
        
    def addObject(self, object: TObject):
        dublicate = False
        
        for obj in Inventory.objects:
            if obj.barcode == object.barcode:
                dublicate=True
                break
            
        if dublicate :
            obj.quantity+=1
            return
        Inventory.objects.append(object)
    
    def removeObject(self, object: TObject):
        for obj in Inventory.objects:
            if obj.barcode == object.barcode:
                break
            
        if obj.quantity > 1:
            obj.quantity -= 1
        
        else:
            Inventory.objects.remove(object)