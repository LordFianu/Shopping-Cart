from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.http import HttpResponse
from .forms import ProductForm

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    context ={
        'products': products
    }
    return render(request, 'cart/index.html', context)

def add_item(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)   # include FILES for images
        if form.is_valid():
            form.save()
            return redirect("home")   # redirect anywhere you want
    else:
        form = ProductForm()

    return render(request, "cart/add_item.html", {"form": form})


def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context ={
        'cart_items': cart_items, 
        'total_price': total_price
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # delete if last item

    return redirect('cart:view_cart')

def home(request):
    return HttpResponse('Hello, World!')