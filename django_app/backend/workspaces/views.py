from uuid import UUID
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Workspace
from .serializers import WorkspaceSerializer

from rest_framework.views import APIView
from rest_framework import status

class WorkspaceManager(APIView):
 
    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
   
    def post(self, request):
        serializer = WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   
   
    def get(self, request, *args, **kwargs):
        uuid = None
        try:
            uuid = request.query_params["uuid"]
        except:
            pass
        print(type(uuid),uuid)
        if uuid:
            workspace = Workspace.objects.get(workspace_uuid=uuid)
            serializer = WorkspaceSerializer(workspace)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
 
        workspaces = Workspace.objects.all()
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
 
    def put(self, request):
        uuid = None
        try:
            uuid = request.query_params["uuid"]
        except:
            pass
        workspace = Workspace.objects.get(workspace_uuid=uuid)
        serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})
 
 
    def delete(self, request, uuid=None):
        uuid = None
        try:
            uuid = request.query_params["uuid"]
        except:
            pass
        workspace = get_object_or_404(Workspace, workspace_uuid=uuid)
        workspace.delete()
        return Response({"status": "success", "data": "student Deleted"})
   
