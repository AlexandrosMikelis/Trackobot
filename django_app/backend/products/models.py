from django.db import models

import uuid
import sys

from workspaces.models import Workspace

TYPES = {
    ("Pharmacy","PHARMACY")
}
# Create your models here.
class Product(models.Model):

    product_uuid = models.AutoField(primary_key = True)
    
    name = models.CharField(max_length=40,null=True)
    barcode = models.CharField(max_length=48,null=True)
    quantity = models.IntegerField(null=True)
    type = models.CharField(choices=TYPES,max_length=30,null=True)
    In = models.BooleanField(default=False)
    Out = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    
    workspace_uuid = models.ForeignKey(Workspace,on_delete=models.CASCADE,null=True)
    
    class Meta:
        db_table = "products"
    
    def __str__(self):
        return self.name
    
    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"

    
