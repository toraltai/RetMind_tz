from django.http import HttpResponse
from django.views import View

from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from config.permissions import IsAuthenticatedViaJWT
from .serializers import *
from .models import *

from openpyxl import Workbook
from io import BytesIO

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedViaJWT]

class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedViaJWT]
    

class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedViaJWT]

class TagDestroyAPIView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedViaJWT]


class ProductAPI(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category').prefetch_related('tags')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedViaJWT]

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ExcelExportView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        wb = Workbook()
        ws = wb.active
        ws.title = "Products"

        ws.append(["Name", "Category", "Tags", "Description", "Price", "Created Date"])

        for product in products:
            tags = ", ".join(tag.name for tag in product.tags.all())
            created_date_naive = product.created_at.replace(tzinfo=None)
            created_date_str = created_date_naive.strftime("%Y-%m-%d %H:%M:%S")
            price = str(round(product.price, 2))
            ws.append([product.name, product.category.name, tags, product.description, price, created_date_str])

        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=product_list.xlsx"
        response.write(excel_file.read())

        return response