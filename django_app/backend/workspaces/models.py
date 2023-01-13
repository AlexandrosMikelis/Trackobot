from django.db import models

import uuid


TYPES = {
    ("Closet","CLOSET"),
    ("Cabinet","CABINET"),
    ("Shelf","sHELF"),
}
# Create your models here.
class Workspace(models.Model):

    workspace_uuid = models.AutoField(primary_key = True)
    
    name = models.CharField(max_length=40,null=True)
    polygon = models.JSONField(null=True)
    coordinates = models.JSONField(null=True)
    type = models.CharField(choices=TYPES,max_length=30,null=True)
    ioCrossline = models.JSONField(null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        db_table = "workspaces"
    
    def __str__(self):
        return self.name

    
