from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Banner(models.Model):
    PAGE_CHOICES = (
        ('home', 'Home Page'),
        ('products', 'Products Page'),
        ('about', 'About Page'),
    )

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    page = models.CharField(max_length=50, choices=PAGE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        return self.product.price * self.quantity
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100, default="Kerala")   
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.full_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    
    def __str__(self):
        return self.user.username

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
class Coupon(models.Model):

    DISCOUNT_TYPE_CHOICES = (
        ('flat', 'Flat'),
        ('percent', 'Percentage'),
    )

    code = models.CharField(max_length=50, unique=True)

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField()

    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    usage_limit = models.IntegerField(default=1)

    used_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    

class Notification(models.Model):

    NOTIFICATION_TYPE = [
        ('order', 'Order'),
        ('customer', 'Customer'),
        ('stock', 'Stock'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    order_id = models.IntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title












