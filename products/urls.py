from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

r = DefaultRouter()

r.register('product', ProductAPI)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<int:pk>/', CategoryDestroyAPIView.as_view()),
    path('tag/', TagListCreateAPIView.as_view()),
    path('tag/<int:pk>/', TagDestroyAPIView.as_view()),
    path('', include(r.urls)),
    path('export-excel/', ExcelExportView.as_view()),
]