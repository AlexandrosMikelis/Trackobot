from django.urls import path

from . import views 

# /api/products/
urlpatterns = [
    path('',views.WorkspaceManager.as_view()),
    path(r'^task\/(?P<pk>.+)$', views.WorkspaceManager.as_view()),
    # path('<int:pk>/update/', views.product_update_view, name='product-edit'),
    # path('<int:pk>/delete/', views.product_destroy_view),
    # path('<int:pk>/', views.product_detail_view, name='product-detail')
]