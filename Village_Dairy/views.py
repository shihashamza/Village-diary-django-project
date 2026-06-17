from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm,BannerForm
from .models import Product,Banner,Address,UserProfile
from .models import Category
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from .models import Product, Cart
from .forms import UserUpdateForm, ProfileUpdateForm
import stripe
from django.http import HttpResponse
from .models import Cart
from django.utils import timezone
from .models import Order
import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    banners = Banner.objects.filter(page='home', is_active=True)
    return render(request, 'home.html', {
        'banners': banners
    })

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def accounts(request):
    return render(request, 'accounts.html')

def milk(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            category="Milk",
            name__icontains=query
        )
    else:
        products = Product.objects.filter(category="Milk")

    return render(request, 'milk.html', {'products': products})

def cheese(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            category="Cheese",
            name__icontains=query
        )
    else:
        products = Product.objects.filter(category="Cheese")

    return render(request, "cheese.html", {"products": products})

def fermented_creamy(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            category="Fermented",
            name__icontains=query
        )
    else:
        products = Product.objects.filter(category="Fermented")

    return render(request, 'fermented_creamy.html', {"products": products})

def fat_based(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            category="Fat-based",
            name__icontains=query
        )
    else:
        products = Product.objects.filter(category="Fat-based")

    return render(request, 'fat_based.html', {"products": products})

def frozen_dairy(request):
    return render(request, 'frozen_dairy.html')

def special_items(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            category="Special",
            name__icontains=query
        )
    else:
        products = Product.objects.filter(category="Special")

    return render(request, 'special_items.html', {"products": products})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')

    total_amount = sum(o.total_amount for o in orders)
    total_orders = orders.count()

    return render(request, 'orders.html', {
        'orders': orders,
        'total_amount': total_amount,
        'total_orders': total_orders,
    })

# @login_required
# def orders(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')

#     return render(request, 'orders.html', {
#         'orders': orders
#     })

def profile(request):
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'addresses': addresses
    })

def wishlist(request):
    return render(request, 'wishlist.html')  

def contact(request):
    return render(request, 'contact.html')


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.is_staff:  
#                 login(request, user)
#                 return redirect("admindashboard")
#             else:
#                 messages.error(request, "You are not allowed to access admin panel")
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, "login.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("admindashboard")  
            else:
                return redirect("home")            

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def add_address(request):

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )

        return redirect('profile')  
    
    return render(request, "add_address.html")

def delete_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    
    if request.method == "POST":
        address.delete()
    
    return redirect('profile')
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        request.session['reset_email'] = email
        return redirect('verify_otp')

    return render(request, 'forgot_password.html')


def verify_otp(request):
    return render(request, 'verify_otp.html')


def password_reset(request):
    return render(request,'password_reset.html')


def product_detail(request, id):
    product = Product.objects.get(id=id)

    in_cart = False
    if request.user.is_authenticated:
        in_cart = Cart.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'in_cart': in_cart
    }

    return render(request, 'product_detail.html', context)

def searchproduct(request):
    query = request.GET.get("q")

    if query:
        product = Product.objects.filter(name__icontains=query).first()

        if product:
            return redirect(product.category)

    return redirect("home")

@login_required(login_url='login')
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    
    return redirect(request.META.get('HTTP_REFERER', 'milk'))


@login_required
def cart(request, action=None, cart_id=None):
    if action and cart_id:
        item = get_object_or_404(Cart, id=cart_id, user=request.user)

        if action == "increase":
            item.quantity += 1

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
            else:
                item.delete()
                return redirect('cart')

        item.save()
        return redirect('cart')

    cart_items = Cart.objects.filter(user=request.user)

    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "cart_total": cart_total
    })

@login_required
def remove_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()

    return redirect('cart')

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    # Add new address
    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            pincode=request.POST.get('pincode'),
        )
        return redirect('checkout')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': total,
        'addresses': addresses
    })


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)

        if form.is_valid():
            # SAVE PROFILE (phone etc)
            form.save()

            # SAVE USER (username & email)
            user = request.user
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()

            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    total_amount = 0

    for item in cart_items:
        total_amount += item.product.price * item.quantity

    
    order_ids = []

    for item in cart_items:
        order = Order.objects.create(
            user=request.user,
            product=item.product,              
            quantity=item.quantity,            
            total_amount=item.product.price * item.quantity,
            payment_method="Online",
            payment_status="Pending",
            status="Order Placed"
        )
        order_ids.append(order.id)

    
    request.session['order_ids'] = order_ids

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': 'Cart Payment'},
                'unit_amount': int(total_amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payment-success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
    )

    return redirect(session.url)

@login_required
def payment_method(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    if request.method == "POST":
        method = request.POST.get('payment_method')

       
        if method == "cod":
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_amount=item.product.price * item.quantity,
                    payment_method="COD",
                    payment_status="Pending",
                    status="Order Placed"
                )

            cart_items.delete()
            return redirect("order_success")

       
        elif method == "online":
            return redirect("pay")   

    return render(request, "payment_method.html")

def payment_success(request):
    order_ids = request.session.get('order_ids')

    if order_ids:
        for oid in order_ids:
            try:
                order = Order.objects.get(id=oid)
                order.payment_status = "Paid"
                order.save()
            except Order.DoesNotExist:
                pass

        request.session.pop('order_ids', None)

    
    Cart.objects.filter(user=request.user).delete()

    return redirect('order_success')
def order_success(request):
    return render(request, 'order_success.html')

#############admin panel###################
@never_cache
def adminlogout(request):
    logout(request)
    return redirect("home")


from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

from django.db.models import Sum
from django.db.models.functions import ExtractMonth

from .models import Product, Order


@never_cache
@staff_member_required(login_url='home')
def admindashboard(request):

    UserModel = get_user_model()

    # Cards
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = UserModel.objects.filter(is_superuser=False).count()
    revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    # Monthly graph data
    monthly_data = (
        Order.objects
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )

    monthly_dict = {i: 0 for i in range(1, 13)}

    for data in monthly_data:
        monthly_dict[data['month']] = float(data['total'] or 0)

    months = list(monthly_dict.keys())
    totals = list(monthly_dict.values())

    max_total = max(totals) if max(totals) > 0 else 1

    sales_data = [
        (
            m,
            round(t, 2),
            round((t / max_total) * 90, 2)
        )
        for m, t in zip(months, totals)
    ]

    return render(request, 'admindashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'revenue': revenue,
        'sales_data': sales_data,
    })

@never_cache
@staff_member_required(login_url='home')
def adminproduct(request):
   
    products = Product.objects.all()
    return render(request, 'adminproduct.html', {'products': products})

@never_cache
@staff_member_required(login_url='home')
def adminaddproduct(request):
  

    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            image1=request.FILES.get("image1"),
            image2=request.FILES.get("image2"),
            image3=request.FILES.get("image3"),
            image4=request.FILES.get("image4"),
        )
        return redirect("adminproduct")

    return render(request, "adminaddproduct.html")

@never_cache
@staff_member_required(login_url='home')
def admineditproduct(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")

        if request.FILES.get("image1"):
            product.image1 = request.FILES.get("image1")

        if request.FILES.get("image2"):
            product.image2 = request.FILES.get("image2")

        if request.FILES.get("image3"):
            product.image3 = request.FILES.get("image3")

        product.save()

        return redirect("adminproduct")

    return render(request, "admineditproduct.html", {"product": product})

@never_cache
@staff_member_required(login_url='home')
def admindeleteproduct(request, id):
    
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect("adminproduct")

@never_cache
@staff_member_required(login_url='home')
def removeimage(request, id):
    

    product = get_object_or_404(Product, id=id)

    product.image1.delete(save=False)
    product.image1 = None
    product.save()

    return redirect("admineditproduct", id=id)

@never_cache
@staff_member_required(login_url='home')
def adminbanner(request):
   
    banners = Banner.objects.all()

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminbanner')
    else:
        form = BannerForm()

    return render(request, 'adminbanner.html', {
        'form': form,
        'banners': banners
    })

@never_cache
@staff_member_required(login_url='home')
def delete_banner(request, id):
    
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    return redirect('adminbanner')



def admincategories(request):
    categories = [choice[0] for choice in Product.CATEGORY_CHOICES]
    return render(request, 'admincategories.html', {
        'categories': categories
    })

@never_cache
@staff_member_required(login_url='home')
def admincoupons(request):
   
    return render(request, 'admincoupons.html')



@never_cache
@staff_member_required(login_url='home')
def admincustomer(request):

    users = User.objects.annotate(
        order_count=Count('order')
    ).order_by('id')   

    data = [
        {
            'user': user,
            'orders': user.order_count
        }
        for user in users
    ]

    return render(request, 'admincustomer.html', {
        'customers': data
    })
@never_cache
@staff_member_required(login_url='home')
def adminnotification(request):
    return render(request, 'adminnotification.html')


@never_cache
@staff_member_required(login_url='home')
def adminorder(request):
    orders = Order.objects.all().order_by('-id')

    print("TOTAL ORDERS:", Order.objects.count())

    return render(request, 'adminorder.html', {
        'orders': orders
    })
    
@never_cache
@staff_member_required(login_url='home')
def adminorderview(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'admin_order_view.html', {'order': order})


@never_cache
@staff_member_required(login_url='home')
def adminorderupdate(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
    return redirect('adminorder')


@never_cache
@staff_member_required(login_url='home')
def adminorderdelete(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('adminorder')



def block_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('admincustomer')

def unblock_user(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('admincustomer')

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('admincustomer')




def add_category(request):

    # ADD CATEGORY
    if request.method == "POST":
        name = request.POST.get('category')
        if name:
            Category.objects.create(name=name)
        return redirect('add_category')

    # GET ALL CATEGORIES
    categories = Category.objects.all()

    return render(request, 'add_category.html', {
        'categories': categories
    })

def update_category(request, id):
    if request.method == "POST":
        name = request.POST.get('category')
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
    return redirect('add_category')

def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('add_category')