from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Product, Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    products = Product.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'products': products})

def product_list(request):
    products = Product.objects.all().order_by('-added_on')  
    return render(request, 'products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if name and price and description and image:
            Product.objects.create(
                user=request.user,  
                name=name,  
                price=price,
                description=description,
                image=image
            )
            messages.success(request, 'Product added successfully')
            return redirect('product_list')
        else:
            messages.error(request, 'All fields are required to be filled')

    return render(request, 'add_product.html')  

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)  

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        messages.success(request, 'Product edited successfully')
        return redirect('product_list')

    return render(request, 'edit_product.html', {'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    product.delete()  
    messages.success(request, 'Product deleted successfully')
    return redirect('product_list')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.user == request.user:
        messages.error(request, "You can't add your own products to the cart!")
        return redirect('product_list')

    if not Cart.objects.filter(user=request.user, product=product).exists():
        Cart.objects.create(user=request.user, product=product)
        messages.success(request, 'Added to cart!')
    else:
        messages.info(request, 'Product already in cart!')

    return redirect('cart_view')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Removed from cart!')
    return redirect('cart_view')
