from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp'),
    path('login/', views.login_view, name='login'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('header/', views.header, name='header'),
    path('navigation/', views.navigation, name='navigation'),
    path('footer/', views.footer, name='footer'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('pre-order-info/', views.pre_order_info, name='pre-order-info'),
    path('about-us/', views.about_us, name='about-us'),
    path('shipping-policy/', views.shipping_policy, name='shipping-policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('refund-policy/', views.refund_policy, name='refund-policy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
]
