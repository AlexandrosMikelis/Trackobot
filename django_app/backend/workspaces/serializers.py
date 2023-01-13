from rest_framework import serializers
from rest_framework.reverse import reverse



from .models import Workspace
# from . import validators

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'