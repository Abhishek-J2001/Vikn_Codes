from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCreateViewSet, ProductListViewSet, StockManagementViewSet, check_subvariant_view


router = DefaultRouter()
router.register(r'products', ProductCreateViewSet, basename='product-create')
router.register(r'product-list', ProductListViewSet, basename='product-list')
router.register(r'stock_management', StockManagementViewSet, basename='stock-management')


urlpatterns = [
    path('', include(router.urls)),
    path('check-subvariant/<int:pk>/', check_subvariant_view, name='check-subvariant'),
]

