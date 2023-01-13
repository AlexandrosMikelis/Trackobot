
class TObject:
    not_given = "Not Given"
    
    def __init__(self,name="",expiration_date = "", rect=[],polygon=[],
                 quantity=1,barcode="",priority="medium",type="general"):
        self.name = name
        self.expiration_date = expiration_date
        self.rect = rect
        self.polygon = polygon
        self.quantity = quantity
        self.barcode = barcode
        self.priority = priority
        self.type = type
    
    def __str__(self):
        return f" Name : {self.name if self.name else TObject.not_given} \n Expiration Date : {self.expiration_date if self.name else TObject.not_given} \n Quantity: {self.quantity if self.quantity else TObject.not_given} \n Barcode: {self.barcode if self.barcode else TObject.not_given} \n Type: {self.type if self.type else TObject.not_given} \n "