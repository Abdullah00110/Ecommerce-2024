from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Customer(models.Model):               # This is Customer model
        user = models.OneToOneField(User, null=True, blank=True,  on_delete=models.CASCADE)
        name = models.CharField(max_length=200, null=True , blank=True)
        email = models.EmailField(max_length=200)

        def __str__(self) -> str:
            return self.name
        

def valid_image_file_ext(value):
    if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
         raise ValidationError("Only PNG, JPG, and JPEG files are allowed.")
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/', validators=[valid_image_file_ext])

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self) -> str:
        return f"Order {self.id} - Transaction: {self.transaction_id or 'N/A'}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product.name} (x{self.quantity}) - Order {self.order.id if self.order else 'N/A'}"
 
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.address}, {self.city}, {self.state} - {self.zipcode}"
