from django.contrib import admin

# import new models **
from .models import User, Cart, Order, Listing, Product, Comment

# Register your models here.

# register models to admin page **
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "password", "is_staff", "is_active", "is_superuser", "last_login", "date_joined")
    filter_horizontal = ("groups", "user_permissions")

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "producer", "title", "category", "price", "stock", "description", "timestamp", "imageurl")
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "producer", "title", "category", "price", "description", "imageurl", "listing", "cart", "order")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment", "listing")

admin.site.register(User, UserAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
