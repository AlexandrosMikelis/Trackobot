from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework import status

# class ProductListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def perform_create(self, serializer):
#         title = serializer.validated_data.get('title')
#         content = serializer.validated_data.get('content') or None
#         if content is None:
#             content = title
#         serializer.save( content=content)

# product_list_create_view = ProductListCreateAPIView.as_view()


# class ProductDetailAPIView(generics.RetrieveAPIView):
    
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    

# product_detail_view = ProductDetailAPIView.as_view()

# class ProductUpdateAPIView(generics.UpdateAPIView):
    
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if not instance.content:
#             instance.content = instance.title


# product_update_view = ProductUpdateAPIView.as_view()

# class ProductDestroyAPIView(generics.DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'

#     def perform_destroy(self, instance):
#         # instance 
#         super().perform_destroy(instance)

# product_destroy_view = ProductDestroyAPIView.as_view()


# class ProductListAPIView(generics.ListAPIView):
    
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
   

# product_list_view = ProductListAPIView.as_view()


# @api_view(['GET', 'POST'])
# def product_alt_view(request, pk=None, *args, **kwargs):
#     method = request.method  

#     if method == "GET":
#         if pk is not None:
#             # detail view
#             obj = get_object_or_404(Product, pk=pk)
#             data = ProductSerializer(obj, many=False).data
#             return Response(data)
#         # list view
#         queryset = Product.objects.all() 
#         data = ProductSerializer(queryset, many=True).data
#         return Response(data)

#     if method == "POST":
#         # create an item
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             title = serializer.validated_data.get('title')
#             content = serializer.validated_data.get('content') or None
#             if content is None:
#                 content = title
#             serializer.save(content=content)
#             return Response(serializer.data)
#         return Response({"invalid": "not good data"}, status=400)
    

class ProductManager(APIView):
 
    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
   
    def post(self, request):
        print(request.data['barcode'])
        try:
            product = Product.objects.get(barcode=request.data['barcode'],workspace_uuid=request.data["workspace_uuid"])
        except:
            product = None
        if product:
            payload = {
                "quantity":product.quantity + 1
            }
            serializer = ProductSerializer(product, data=payload, partial=True)
        else:
            serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   
   
    def get(self, request, uuid=None):
        uuid = None
        try:
            uuid = request.query_params["uuid"]
        except:
            pass
        if uuid:
            product = Product.objects.get(product_uuid=uuid)
            serializer = ProductSerializer(product)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
 
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
 
    def put(self, request, uuid=None):
        uuid = None
        try:
            uuid = request.query_params["uuid"]
        except:
            pass
        student = Product.objects.get(product_uuid=uuid)
        serializer = ProductSerializer(student, data=request.data, partial=True)
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
        student = get_object_or_404(Product, product_uuid=uuid)
        student.delete()
        return Response({"status": "success", "data": "student Deleted"})
   
