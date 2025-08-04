from django.urls import path  
from . import views

urlpatterns=[
    path('books/',views.get_books,name='api-books'),
    path('books/<int:pk>/', views.get_book_details, name='api-book-detail'),
    path('auth/register/', views.api_register, name='api-register'),
    path('auth/login/', views.api_login, name='api-login'),
    path('auth/logout/', views.api_logout, name='api-logout'),

]
