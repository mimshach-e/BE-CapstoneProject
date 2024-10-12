from rest_framework import serializers
from decimal import Decimal
from .models import Category, Product, ProductImage, Rating, WishList, Discount
from django.contrib.auth import get_user_model

User = get_user_model()

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_by', 'created_at'] 
        read_only_fields = ['created_by', 'created_at']  
         

# ProductImage Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


# Discount Serializer
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'name', 'discount_type', 'value', 'start_date', 'end_date',
                  'active', 'product']


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    """ 
    this is creating a many-to-many relationship to the product in order to 
    handle image conversion and send multiple images
    """
    images = ProductImageSerializer(many=True, read_only=True)

    # this is receiving 
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=10000000, allow_empty_file=False, use_url=False),
        write_only=True
        )
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.00'),
                                     max_value=Decimal('1000000.00'))
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discounted_price', 'category',
                  'stock_quantity', 'created_at', 'created_by', 'images', 'uploaded_images']
        read_only_fields = ['created_by', 'created_at', 'images'] 


        # Name validation: Handles validation for name field to prevent empty field or whitespace
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError('Product name cannnot be empty or whitespace')
            return value

        # Price validation: checks price to ensure it's not a zero or negative value
        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError('Price must be greater than zero')
            return value

        # Stock quantity validation: checks to ensure stock quantity is not negative
        def validate_stock_quantity(self, value):
            if value < 0:
                raise serializers.ValidationError('Stock quantity cannot be less than zero')
            return value
        

    def get_discounted_price(self, obj):
            return obj.discounted_price
        
        
    # Handles the process of creating a product with multiple images for each at a go
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product
            

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")

        for attr, value in validated_data.items():
            # Update the product fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()

            # Handle the images
            self._handle_images(instance, uploaded_images)

            return instance

    def _handle_images(self, product, uploaded_images):
        # If there are new images, delete the old ones
        if uploaded_images:
            product.images.all().delete()
        
        # Create new image instances
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
            
       
# Serializer for the Rating Model
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        user_id = self.context['user_id']
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
        rating = Rating.objects.create(product=product, user=user, **validated_data)
        return rating
    


class WishListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), 
                                                    source='product', write_only=True)


    class Meta:
        model = WishList
        fields = ['id', 'product_id', 'product_name', 'user'] 
        read_only_fields = ['user']  

    def create(self, validated_data):
        user = self.context['request'].user
        return WishList.objects.create(user=user, **validated_data)    



           