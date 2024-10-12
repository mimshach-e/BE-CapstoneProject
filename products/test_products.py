from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Category, Product, Rating, WishList, Discount
from .serializers import CategorySerializer, ProductSerializer, RatingSerializer, WishListSerializer, DiscountSerializer
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

class ProductsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@alx.com', password='testing@123')
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@alx.com', password='admin@123')
        
        # create category
        self.category = Category.objects.create(name='Test Category', created_by=self.admin_user)
        
        # create product
        self.product = Product.objects.create(
            name = 'Test Product',
            description = 'This is a test description',
            price = Decimal('100.00'),
            category = self.category,
            stock_quantity = 300,
            created_by = self.admin_user
        )   

    def test_create_category(self):
        # Test with admin user
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category_create')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(name='New Category').created_by, self.admin_user)

        # Test with non-admin user
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Another Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 2)  # Count should not increase

    def test_list_categories(self):
        url = reverse('category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # list category
    def test_list_categories(self):
        url = reverse('category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the response is paginated
        if 'results' in response.data:
            categories = response.data['results']
        else:
            categories = response.data
        
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]['name'], 'Test Category')
        
        print(f"Response data: {response.data}")
        print(f"Number of categories: {len(categories)}")
        print(f"Category data: {categories[0]}")
    
    
    def test_create_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products-create')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '50.00',
            'category': self.category.id,
            'stock_quantity': 20,
            'uploaded_images': []
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(name='New Product').created_by, self.user)


    def test_list_products(self):
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Considering pagination set to 10 per page  


    def test_product_detail(self):
        url = reverse('products-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')        


    def test_update_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products-update', kwargs={'pk': self.product.id})
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': '15.00',
            'category': self.category.id,
            'stock_quantity': 85,
            'uploaded_images': []
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')    

    def test_delete_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products-delete', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)    

    
    def test_create_rating(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-ratings-list', kwargs={'product_id': self.product.id})
        data = {
            'rating': 4,
            'description': 'Great product!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().user, self.user)


    def test_create_wishlist(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-wishlist-list', kwargs={'product_id': self.product.id})
        data = {
            'product_id': self.product.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishList.objects.count(), 1)
        self.assertEqual(WishList.objects.first().user, self.user)

    def test_create_discount(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product-discount-list', kwargs={'product_id': self.product.id})
        data = {
            'name': 'Xmas Bonus',
            'discount_type': 'percentage',
            'value': 10,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=30),
            'active': True,
            'product': [self.product.id]
        }
        response = self.client.post(url, data, format='json')
        
        print(f'response data: {response}') # Print out the response object
        print(response.json()) # Print out the response JSON data

        # Print out the input values being used to calculate the discount
        print("Original price:", self.product.price)

        # Print out the calculated discounted price
        print("Calculated discounted price:", self.product.discounted_price)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discount.objects.count(), 1)
        self.assertEqual(self.product.discounted_price, Decimal('90.00'))


    def test_product_filter(self):
        url = reverse('products-list')
        response = self.client.get(url, {'category': self.category.id, 'price_gte': 5, 'price_lte': 15})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)    


    def test_product_search(self):
        url = reverse('products-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)    


    def test_product_ordering(self):
        url = reverse('products-list')
        response = self.client.get(url, {'ordering': '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

   