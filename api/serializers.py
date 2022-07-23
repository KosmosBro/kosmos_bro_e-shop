from rest_framework import serializers

from main.models import Supplier, Discount, Category, Product, User, Cart, CartContent


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'discount']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    discount = DiscountSerializer(many=True)
    supplier = SupplierSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'description', 'creation_date', 'picture', 'price', 'category', 'discount', 'supplier']

    def create(self, validated_data):
        create_category = validated_data.pop('category')
        create_discount = validated_data.pop('discount')
        create_supplier = validated_data.pop('supplier')
        product = Product.objects.create(**validated_data)

        for category in create_category:
            Category.objects.create(product=product, **category)

        for discount in create_discount:
            Discount.objects.create(product=product, **discount)

        for supplier in create_supplier:
            Supplier.objects.create(product=product, **supplier)
        return product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartContent
        fields = '__all__'
