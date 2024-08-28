from rest_framework import serializers
from .models import Products, Variant, SubVariant

class SubVariantSerializer(serializers.ModelSerializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all())

    class Meta:
        model = SubVariant
        fields = ['id', 'name', 'stock', 'variant']

    def validate(self, data):
        if 'variant' not in data:
            raise serializers.ValidationError({'variant': 'This field is required.'})
        return data

class SubVariantNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['id', 'name', 'stock']

class VariantSerializer(serializers.ModelSerializer):
    subvariants = SubVariantNestedSerializer(many=True, required=False)

    class Meta:
        model = Variant
        fields = ['id', 'name', 'options', 'subvariants']

class ProductCreateSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Products
        fields = [
            'ProductID', 'ProductCode', 'ProductName', 'ProductImage', 'CreatedDate',
            'CreatedUser', 'IsFavourite', 'Active', 'HSNCode',
            'TotalStock', 'variants'
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        product = Products.objects.create(**validated_data)
        for variant_data in variants_data:
            subvariants_data = variant_data.pop('subvariants', [])
            variant = Variant.objects.create(product=product, **variant_data)
            for subvariant_data in subvariants_data:
                SubVariant.objects.create(variant=variant, **subvariant_data)
        return product

class StockUpdateSerializer(serializers.Serializer):
    stock = serializers.DecimalField(max_digits=20, decimal_places=8)

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock value cannot be negative.")
        return value

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'ProductID', 'ProductCode', 'ProductName', 'ProductImage',
            'CreatedDate', 'UpdatedDate', 'CreatedUser', 'IsFavourite', 
            'Active', 'HSNCode', 'TotalStock'
        ]
