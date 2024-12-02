from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings

# Mock user data
users = {
    "admin": "password123"
}

# Example data structure
products = {
    "Pokémon": {
        "Sealed Product": {
            "Booster Packs": ["Example Pack 1", "Example Pack 2"],
            "Booster Boxes": ["Example Box 1", "Example Box 2"],
            "Elite Trainer Boxes": ["Example Trainer Box 1", "Example Trainer Box 2"],
            "Tins": ["Example Tin 1", "Example Tin 2"],
        },
        "Opened Product": {
            "Series 1": ["Expansion 1A", "Expansion 1B"],
            "Series 2": ["Expansion 2A", "Expansion 2B"],
        },
    },
    "Accessories": ["Sleeves", "Binders", "Deck Boxes"],
}

# Views
# Store OTP in session for verification
def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Generate OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['password'] = password

        # Send OTP via email
        send_mail(
            'Your OTP for TCG Store Registration',
            f'Your OTP is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('verify-otp')

    return render(request, 'store/portal/signup.html')


# OTP verification view
def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        session_otp = request.session.get('otp')
        email = request.session.get('email')
        password = request.session.get('password')

        if str(entered_otp) == str(session_otp):
            # Create user after OTP verification
            user = User.objects.create_user(username=email, email=email, password=password)
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, 'store/portal/verify_otp.html')

def login_view(request):
    # If the user is already authenticated, redirect to the profile page
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to profile if logged in

    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Redirect to profile after successful login
        else:
            error = "Invalid username or password. Please try again."

    return render(request, 'store/portal/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'store/header/profile.html')

def home(request):
    category = request.GET.get("category", "Pokémon")
    subcategory = request.GET.get("subcategory")
    subsubcategory = request.GET.get("subsubcategory")
    current_data = products.get(category, {})

    if subcategory:
        current_data = current_data.get(subcategory, {})
    if subsubcategory:
        current_data = current_data.get(subsubcategory, {})

    return render(request, 'store/dashboard.html', {
        "category": category,
        "subcategory": subcategory,
        "subsubcategory": subsubcategory,
        "current_data": current_data,
        "products": products,
        'tiles': range(1, 28),
    })

def settings_view(request):
    return render(request, "store/header/settings.html")

# Component Views
def header(request):
    return render(request, 'store/header.html')

def navigation(request):
    return render(request, 'store/navigation.html')

def footer(request):
    return render(request, 'store/footer.html')

# Footer pages
def contact_us(request):
    return render(request, 'store/footer/contact-us.html')

def pre_order_info(request):
    return render(request, 'store/footer/pre-order-info.html')

def about_us(request):
    return render(request, 'store/footer/about-us.html')

def shipping_policy(request):
    return render(request, 'store/footer/shipping-policy.html')

def privacy_policy(request):
    return render(request, 'store/footer/privacy-policy.html')

def refund_policy(request):
    return render(request, 'store/footer/refund-policy.html')

def terms_of_service(request):
    return render(request, 'store/footer/terms-of-service.html')
