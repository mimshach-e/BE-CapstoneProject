from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
    
    

# Discount Model    
class Discount(models.Model):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    DISCOUNT_TYPE = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed Amount'),
    ]

    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=15, choices=DISCOUNT_TYPE, default=PERCENTAGE)
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0), MaxValueValidator(100 if discount_type == PERCENTAGE else 99999)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    product = models.ManyToManyField('Product', related_name='discounts')

    def __str__(self):
        return self.name    


# Product Model.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.DecimalField(null=False, max_digits=8, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0, null=False)
    #image = models.ImageField(null=True, editable=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def reduce_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
        else:
            raise ValidationError(f"Not enough stock. Available stock is {self.stock_quantity}")    
    
    # Discount Property
    @property
    def discounted_price(self):
        active_discount = self.discounts.filter(active=True, start_date__lte=timezone.now(), 
                                                end_date__gte=timezone.now()).first()
        if active_discount:
            if active_discount.discount_type == Discount.PERCENTAGE:
                return self.price * (1 - active_discount.value / 100)
            elif active_discount.discount_type == Discount.FIXED:
                return max(self.price - active_discount.value, 0)
        return self.price            


# Product Image Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, editable=True)


# Rating Model
class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated')
    rating = models.PositiveIntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        return f"Rating: {self.user} gave {self.rating}-star to {self.product}"    
    

class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']



    

   