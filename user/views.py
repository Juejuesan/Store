from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileRegisterForm
from .models import Post, Order, Profile
from decimal import Decimal


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('user:dashboard')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    return render(request, 'user/register.html', {'user_form': user_form, 'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('user:login')


@login_required
def dashboard_view(request):
    posts = Post.objects.exclude(seller=request.user)
    my_posts = Post.objects.filter(seller=request.user)
    orders = Order.objects.filter(buyer=request.user)
    profile = request.user.profile

    # ပထမဆုံးအကြိမ် ဝယ်ယူသူ ဟုတ်/မဟုတ် စစ်ဆေးခြင်း
    has_previous_orders = Order.objects.filter(buyer=request.user).exists()
    discount_applicable = not has_previous_orders

    return render(request, 'user/dashboard.html', {
        'profile': profile,
        'posts': posts,
        'my_posts': my_posts,
        'orders': orders,
        'discount_applicable': discount_applicable
    })


@login_required
def top_up(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))
        if amount > 0:
            profile = request.user.profile
            profile.balance += amount
            profile.save()
            messages.success(request, f"Successfully topped up {amount} Kyats!")
    return redirect('user:dashboard')


@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))
        profile = request.user.profile
        if 0 < amount <= profile.balance:
            profile.balance -= amount
            profile.save()
            messages.success(request, f"Successfully withdrew {amount} Kyats!")
        else:
            messages.error(request, "Insufficient balance or invalid amount.")
    return redirect('user:dashboard')


@login_required
def sell_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = Decimal(request.POST.get('price', '0'))
        if title and price > 0:
            Post.objects.create(seller=request.user, title=title, description=description, price=price)
            messages.success(request, "Item posted for sale successfully!")
    return redirect('user:dashboard')


@login_required
def buy_item(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = request.user.profile
    original_price = post.price
    final_price = original_price
    discount_applied = False

    has_orders = Order.objects.filter(buyer=request.user).exists()
    if not has_orders:
        final_price = original_price * Decimal('0.90')  # 10% Discount applied
        discount_applied = True

    if profile.balance >= final_price:
        profile.balance -= final_price
        profile.save()

        Order.objects.create(buyer=request.user, post=post, final_price=final_price, discount_applied=discount_applied)

        seller_profile = post.seller.profile
        seller_profile.balance += final_price
        seller_profile.save()

        post.delete()

        if discount_applied:
            messages.success(request, f"First-time Purchase! 10% Discount Applied! Paid {final_price} Kyats.")
        else:
            messages.success(request, f"Successfully purchased for {final_price} Kyats.")
    else:
        messages.error(request, "Insufficient balance. Please Top Up first!")

    return redirect('user:dashboard')