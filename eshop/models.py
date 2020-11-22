from django.db import models

# import abstract user model **
from django.contrib.auth.models import AbstractUser

# Create your models here.

# new models **
# user model **
class User(AbstractUser):
    # followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers_ref") - for follower implementation
    # following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following_ref") (OPTIONAL)

    def __str__(self):
        return f"{self.username} {self.email}"

# cart model **
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    
    def __str__(self):
        return f"{self.user.username}'s Cart"

# order model **
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=100)
    creditcard = models.CharField(max_length=64)
    confirmation = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.confirmation} by {self.user.username}"

# listing model **
class Listing(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField()
    description = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    imageurl = models.CharField(max_length=100000)

    def __str__(self):
        return f"{self.title} by: {self.producer} on {self.timestamp} stock: {self.stock}"

# product model **
class Product(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=500)
    imageurl = models.CharField(max_length=100000)

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="products")

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products", null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products", null=True)

    def __str__(self):
        return f"{self.title} by: {self.producer.username} (product)"

# comment model **
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)
    comment = models.CharField(max_length=500) 
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"'{self.comment}' by {self.user.username}"