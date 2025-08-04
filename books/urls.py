from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.index,name="home"),
    path('login',views.loginUser,name="login"),
    path('product_details/<int:id>/', views.product_details, name="product_details"),
    path('signup',views.signup,name="signup"),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:book_id>/', views.buy_now, name='buy_now'),
    path('logout/', views.logoutUser, name='logout'),
    path('api/',include('books.api_urls')),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
      
    # Checkout for individual book
    path('checkout/<int:book_id>/', views.checkout, name='checkout'),
    # Checkout for all books in the cart
    path('checkout/', views.checkout_all, name='checkout_all'),
    # success URL
    path('checkout/success/', views.checkout_success, name='checkout_success'),


]
