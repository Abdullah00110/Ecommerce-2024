from django.shortcuts import render
from .models import *
# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'store/store.html', context)          # ------> views for store
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        context = {'items': items}
    else:
        items = []
        context = {'items': items}

    return render(request, 'store/cart.html', context)           # --------> views for cart

def checkout(request):
    return render(request, 'store/checkout.html')                # ----------> views for checkout
