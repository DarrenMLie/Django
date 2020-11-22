from django.shortcuts import render

# import other functions **
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# import other models **
from .models import User, Cart, Order, Listing, Product, Comment

# import paginator **
from django.core.paginator import Paginator

# import login decorator **
from django.contrib.auth.decorators import login_required

# import json response **
from django.http import JsonResponse

# import csrf exempt **
from django.views.decorators.csrf import csrf_exempt

# import json **
import json

# import Q objects **
from django.db.models import Q

# import random **
import random

# Create your views here.

# index view **
def index(request):
    # get all listings **
    listings = Listing.objects.all()
    # sort by most recent listing first **
    listings.order_by("-timestamp").all()

    return render(request, 'eshop/index.html', {
        "listings": listings
    })

# login view **
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('eshop:index'))
        else:
            return render(request, 'eshop/login.html', {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, 'eshop/login.html')

# logout view **
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('eshop:index'))

# register view **
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, 'eshop/register.html', {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # create a cart for the user **
            cart = Cart(user=user)
            cart.save()
        except IntegrityError:
            return render(request, 'eshop/register.html', {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('eshop:index'))
    else:
        return render(request, 'eshop/register.html')

# add listing view **
def add(request):
    if request.method == "POST":
        # get information from request **
        producer = request.user
        title = request.POST.get("title").capitalize()
        category = request.POST.get("category").capitalize()
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        description = request.POST.get("description")
        imageurl = request.POST.get("imageurl")

        # create new listing **
        listing = Listing(producer=producer, title=title, category=category, price=price, stock=stock, description=description, imageurl=imageurl)
        listing.save()

        # create products based on listingstock **
        for i in range(int(stock)):
            product = Product(producer=producer, title=title, category=category, price=price, description=description, imageurl=imageurl, listing=listing)
            product.save()
        
        # redirect to index page **
        return HttpResponseRedirect(reverse('eshop:index'))

    # render add page if get request **
    return render(request, 'eshop/add.html')

# listing view **
@login_required(login_url='eshop:login')
def listing(request, listing_id):
    # get listing **
    listing = Listing.objects.get(pk=listing_id)

    # get user's cart **
    cart = request.user.cart
    cart_products = cart.products.all()

    # listing's products in user cart **
    products_in_cart = 0
    for product in cart_products:
        if product.listing == listing:
            products_in_cart += 1

    return render(request, "eshop/listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "products_in_cart": products_in_cart
    })

# categories view **
def categories(request):
    # render available categories **
    return render(request, 'eshop/categories.html')

# category listings view **
def category(request, category):
    # get all listings and filter them **
    listings = Listing.objects.filter(category=category.capitalize())
    # sort by most recent listing first **
    listings.order_by("-timestamp").all()

    return render(request, 'eshop/category.html', {
        "listings": listings,
        "category": category.capitalize()
    })

# comments view ** JS
@csrf_exempt
def comment(request, listing_id):
    if request.method == "POST":
        # load json body **
        data = json.loads(request.body)
        comment = data.get("comment", "")

        # create new comment **
        comment = Comment(user=request.user, comment=comment, listing=Listing.objects.get(pk=listing_id))
        comment.save()

        return JsonResponse({"message": "Comment added to listing successfully."}, status=201)

    # redirect to listing page **
    return HttpResponseRedirect(reverse('eshop:listing', args=(listing_id,)))

# search view **
def search(request):
    # get query and listing **
    query = request.GET.get("query")
    listings = Listing.objects.all()
    # sort by most recent listing first **
    listings.order_by("-timestamp").all()

    # check is query in listing's title **
    results = []
    for listing in listings:
        if query in listing.title or query.capitalize() in listing.title:
            results.append(listing)

    return render(request, 'eshop/search.html', {
        "listings": results
    })

# cart view ** JS
@csrf_exempt
def cart(request):
    if request.method == "POST":
        # get data **
        data = json.loads(request.body)
        # for adding **
        listing_id = data.get("listing_id", "")
        amount = data.get("amount", "")
        # for removing **
        product_id = data.get("product_id", "")

        # adding products to cart**
        if not product_id:
            # get listing & products **
            listing = Listing.objects.get(pk=listing_id)
            products = listing.products.all()[:int(amount)]
            # add products to user cart **
            for product in products:
                request.user.cart.products.add(product)

            # return HttpResponseRedirect(reverse('eshop:listing', args=(listing_id,)))
            return JsonResponse({"message": "Products added to cart successfully."}, status=201)

        # removing product from cart **
        else:
            product = Product.objects.get(pk=product_id)
            request.user.cart.products.remove(product)

            return JsonResponse({"message": "Product removed from cart successfully."}, status=201)

    # get user's cart **
    cart = request.user.cart
    cart_products = cart.products.all()
    # calculate cart subtotal **
    subtotal = 0
    for product in cart_products:
        subtotal += product.price

    return render(request, 'eshop/cart.html', {
        "cart_products": cart_products,
        "subtotal": subtotal
    })

# checkout view **
def checkout(request):
    if request.method == "POST":
        # get info **
        total = request.POST.get("total")[1:]
        address = request.POST.get("address")
        creditcard = request.POST.get("creditcard")
        confirmation = random.randint(1000000000, 9999999999)

        # create new order **
        order = Order(user=request.user, total=total, address=address, creditcard=creditcard, confirmation=confirmation)
        order.save()

        # move items from cart into order and remove items from cart **
        cart = request.user.cart
        cart_products = cart.products.all()
        for product in cart_products:
            # add product to order **
            order.products.add(product)
            # remove product from cart **
            cart.products.remove(product)
            # subtract from listing stock **
            listing = product.listing
            listing.stock = listing.stock - 1
            listing.save()

        # redirect to order view **
        return HttpResponseRedirect(reverse('eshop:order', args=(order.id,)))

    cart = request.user.cart
    cart_products = cart.products.all()
    # calculate cart subtotal **
    total = 0
    for product in cart_products:
        total += product.price

    return render(request, 'eshop/checkout.html', {
        "cart_products": cart_products,
        "total": total
    })

# order view **
def order(request, order_id):
    # get order **
    order = Order.objects.get(pk=order_id)

    return render(request, 'eshop/order.html', {
        "order": order
    })

# orders view **
def orders(request):
    # get and filter orders **
    orders = Order.objects.filter(user=request.user)
    # sort by most recent order first **
    orders.order_by("-timestamp").all()

    return render(request, 'eshop/orders.html', {
        "orders": orders
    })

# profile view **
def profile(request, username):
    profile_user = User.objects.get(username=username)
    listings = Listing.objects.filter(producer=profile_user)
    # sort by most recent listing first **
    listings.order_by("-timestamp").all()

    # get oldest listing **
    first_listing_date = listings.last()

    return render(request, "eshop/profile.html", {
        "profile_user": profile_user,
        "listings": listings,
        "first_listing_date": first_listing_date.timestamp
    })






