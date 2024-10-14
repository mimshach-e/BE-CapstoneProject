# BE-CapstoneProject
This is an E-commerce Product API that enables CRUD operations for products, advanced category management, product reviews, multiple images, and search by name or category. It includes Wishlist management, automatic stock reduction upon purchase, and discount functionality. Built based on Django ORM, it's deployable on Heroku or PythonAnywhere etc.


# E-commerce Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Accounts App](#accounts-app)
   - [Models](#accounts-models)
   - [Admin](#accounts-admin)
   - [Serializers](#accounts-serializers)
   - [Views](#accounts-views)
   - [URLs](#accounts-urls)
3. [Products App](#products-app)
   - [Models](#products-models)
   - [Admin](#products-admin)
   - [Serializers](#products-serializers)
   - [Views](#products-views)
   - [Filters](#products-filters)
   - [URLs](#products-urls)

## 1. Project Overview <a name="project-overview"></a>

This project is an e-commerce platform built using Django and Django Rest Framework. It consists of two main apps: `accounts` and `products`. The `accounts` app handles user management, while the `products` app manages product-related functionality including categories, discounts, ratings, and wishlists.

## 2. Accounts App <a name="accounts-app"></a>

The `accounts` app is responsible for user management, including registration, authentication, and authorization.

### Models <a name="accounts-models"></a>

#### CustomUser
- Extends `AbstractBaseUser` and `PermissionsMixin`
- Fields:
  - `username`: CharField, unique
  - `email`: EmailField, unique
  - `is_active`: BooleanField
  - `is_staff`: BooleanField
  - `date_joined`: DateTimeField
  - `user_permissions`: ManyToManyField to `Permission`

#### CustomUserManager
- Extends `BaseUserManager`
- Methods:
  - `create_user`: Creates a regular user
  - `create_superuser`: Creates a superuser

### Admin <a name="accounts-admin"></a>

- CustomUserAdmin: Customizes the admin interface for the CustomUser model

### Serializers <a name="accounts-serializers"></a>

#### CustomUserSerializer
- Serializes the CustomUser model
- Hashes the password during user creation

#### LoginSerializer
- Handles user login
- Validates username and password

### Views <a name="accounts-views"></a>

#### UserRegistrationView
- Allows new users to register
- Uses CustomUserSerializer

#### UserLoginView
- Handles user login
- Uses LoginSerializer
- Returns user data and login status

### URLs <a name="accounts-urls"></a>

- `/accounts/register/`: User registration endpoint
- `/accounts/login/`: User login endpoint

## 3. Products App <a name="products-app"></a>

The `products` app manages all product-related functionality, including categories, discounts, ratings, and wishlists.

### Models <a name="products-models"></a>

#### Category
- Fields:
  - `name`: CharField, unique
  - `created_by`: ForeignKey to User
  - `created_at`: DateTimeField

#### Discount
- Fields:
  - `name`: CharField
  - `discount_type`: CharField (choices: Percentage or Fixed Amount)
  - `value`: DecimalField
  - `start_date`: DateTimeField
  - `end_date`: DateTimeField
  - `active`: BooleanField
  - `product`: ManyToManyField to Product

#### Product
- Fields:
  - `name`: CharField
  - `description`: TextField
  - `price`: DecimalField
  - `category`: ForeignKey to Category
  - `stock_quantity`: PositiveIntegerField
  - `created_at`: DateTimeField
  - `created_by`: ForeignKey to User
- Methods:
  - `reduce_stock`: Reduces the stock quantity
  - `discounted_price`: Property that calculates the discounted price

#### ProductImage
- Fields:
  - `product`: ForeignKey to Product
  - `image`: ImageField

#### Rating
- Fields:
  - `product`: ForeignKey to Product
  - `user`: ForeignKey to User
  - `rating`: PositiveIntegerField (1-5 stars)
  - `description`: TextField
  - `created_at`: DateTimeField

#### WishList
- Fields:
  - `product`: ForeignKey to Product
  - `user`: ForeignKey to User
  - `created_at`: DateTimeField

### Admin <a name="products-admin"></a>

- ProductAdmin: Customizes the admin interface for the Product model
- CategoryAdmin: Customizes the admin interface for the Category model
- DiscountAdmin: Customizes the admin interface for the Discount model

### Serializers <a name="products-serializers"></a>

#### CategorySerializer
- Serializes the Category model

#### ProductImageSerializer
- Serializes the ProductImage model

#### DiscountSerializer
- Serializes the Discount model

#### ProductSerializer
- Serializes the Product model
- Handles multiple image uploads
- Includes validation for name, price, and stock quantity

#### RatingSerializer
- Serializes the Rating model

#### WishListSerializer
- Serializes the WishList model

### Views <a name="products-views"></a>

#### Category Views
- CreateCategoryView: Creates a new category
- ListCategoryView: Lists all categories
- DetailCategoryView: Retrieves a specific category
- UpdateCategoryView: Updates a category
- DeleteCategoryView: Deletes a category

#### Product Views
- CreateProductView: Creates a new product
- ListProductView: Lists all products with filtering, searching, and pagination
- DetailProductView: Retrieves a specific product
- UpdateProductView: Updates a product
- DeleteProductView: Deletes a product

#### RatingView
- Handles CRUD operations for product ratings

#### WishListView
- Handles CRUD operations for user wishlists

#### DiscountView
- Handles CRUD operations for product discounts

### Filters <a name="products-filters"></a>

#### ProductFilter
- Allows filtering products by category, price range, and stock quantity

### URLs <a name="products-urls"></a>

- Category endpoints:
  - `/category/create/`
  - `/category/`
  - `/category/<int:pk>/`
  - `/category/<int:pk>/update/`
  - `/category/<int:pk>/delete/`

- Product endpoints:
  - `/products/create/`
  - `/products/`
  - `/products/<int:pk>/`
  - `/products/<int:pk>/update/`
  - `/products/<int:pk>/delete/`

- Rating, WishList, and Discount endpoints:
  - `/products/<int:product_id>/ratings/`
  - `/products/<int:product_id>/wishlist/`
  - `/products/<int:product_id>/discounts/`

## Conclusion

This e-commerce project provides a robust backend for managing users, products, categories, discounts, ratings, and wishlists. It uses Django's powerful ORM and Django Rest Framework's serializers and views to create a RESTful API. The project is well-structured, with clear separation of concerns between the `accounts` and `products` apps.

Key features include:
- Custom user model with JWT authentication
- Product management with categories and multiple images
- Discount system with percentage and fixed amount options
- Rating system for products
- Wishlist functionality for users
- Filtering, searching, and pagination for product listings

This documentation provides an overview of the project structure and main components. For more detailed information, refer to the individual files and their inline comments.