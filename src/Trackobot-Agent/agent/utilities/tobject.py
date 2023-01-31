
class TObject(object):
    
    def __init__(self, id, barcode, rect, state="UNKNOWN", exp_date="", name=""):
        
        self.id = id
        self.state = state
        self.barcode = barcode
        self.exp_date = exp_date
        self.rect = rect
        self.name = name
    
    def __repr__(self):
        return f"TObject({self.id}, {self.barcode}, {self.state}, {self.rect}, {self.state}, {self.exp_date}, {self.name})"
        
    def __str__(self):
        return f"Name: {self.name} Barcode: {self.barcode} State: {self.state}"