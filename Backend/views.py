from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Products, SubVariant
from .serializers import ProductCreateSerializer, ProductListSerializer, StockUpdateSerializer, SubVariantSerializer

class ProductCreateViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductCreateSerializer

class ProductListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductListSerializer

class StockManagementViewSet(viewsets.ModelViewSet):
    queryset = SubVariant.objects.all()
    serializer_class = SubVariantSerializer

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        """
        Adds stock to a specific subvariant.
        """
        try:
            subvariant = self.get_object() 
            serializer = StockUpdateSerializer(data=request.data)
            if serializer.is_valid():
                stock_to_add = serializer.validated_data['stock']
                if stock_to_add < 0:
                    return Response({"error": "Stock value cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
                subvariant.stock += stock_to_add
                subvariant.save()
                return Response({"status": "Stock added", "current_stock": subvariant.stock}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SubVariant.DoesNotExist:
            return Response({"error": "SubVariant not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_stock(self, request, pk=None):
        """
        Removes stock (for sale) from a specific subvariant.
        """
        try:
            subvariant = self.get_object()  
            serializer = StockUpdateSerializer(data=request.data)
            if serializer.is_valid():
                stock_to_remove = serializer.validated_data['stock']
                if stock_to_remove < 0:
                    return Response({"error": "Stock value cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
                if stock_to_remove > subvariant.stock:
                    return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)
                subvariant.stock -= stock_to_remove
                subvariant.save()
                return Response({"status": "Stock removed", "current_stock": subvariant.stock}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SubVariant.DoesNotExist:
            return Response({"error": "SubVariant not found"}, status=status.HTTP_404_NOT_FOUND)

def check_subvariant_view(request, pk):
    subvariant = SubVariant.objects.filter(pk=pk).first()
    if subvariant:
        return JsonResponse({'subvariant': str(subvariant)})
    return JsonResponse({'error': 'SubVariant not found'}, status=404)
