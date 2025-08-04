from urllib import request
from django.shortcuts import render,get_object_or_404,redirect
from .models import Book,Cart
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from django.db.models import Q
# Create your views here.
def index(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, "index.html", {'books': books})
def loginUser(request):
    if request.method=='POST':
        uName=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=uName,password =pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Login successful")
            next_url = request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')

        

    return render(request,"login.html")


def logoutUser(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        username=request.POST.get('username')
        pwd=request.POST.get('password')
        confpwd=request.POST.get('confirmpwd')
        if pwd!=confpwd:
            messages.error(request,"Password do not match")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
             messages.error(request,"Username already exists")
             return redirect('signup')
        
        user=User.objects.create_user(
            username=username,
            email=email,
            password=pwd
            )
        user.save()
        login(request,user)
        messages.success(request,"Registration successful")
        return redirect('/')


    return render(request,"register.html")
        
@login_required(login_url='login')
def product_details(request,id):
    bookDetails=get_object_or_404(Book,pk=id)
    print(bookDetails.cover_image)
    return render(request,"product_details.html",{"book":bookDetails})

def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{book.title} has been added to your cart.")
    return redirect('cart')
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required(login_url='login')
def remove_from_cart(request, book_id):
    try:
        item = Cart.objects.get(user=request.user, book_id=book_id)
        item.delete()
        messages.success(request, "✅ Book removed from cart.")
    except Cart.DoesNotExist:
        messages.error(request, "❌ Book not found in your cart.")
    return redirect('cart')



@login_required(login_url='login')
def checkout(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        # ... handle form submission
        return redirect('checkout_success')

    return render(request, 'checkout.html', {'book': book, 'mode': 'single'})
@login_required(login_url='login')
def checkout_all(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        # ... handle form submission
        return redirect('checkout_success')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'mode': 'cart'})

def checkout_success(request):
    return render(request, 'checkout_success.html')
@login_required
def buy_now(request, book_id):
     book = get_object_or_404(Book, pk=book_id)
     if request.method == 'POST':
         return redirect('checkout_success')
     return render(request, 'checkout.html', {'book': book, 'mode': 'single'})



#************Api*******
@api_view(['GET'])
def get_books(request):
    books=Book.objects.all()
    serializer=BookSerializer(books,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_book_details(request,pk):
    try:
        book=Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response({"error":"Book not found"},status = 404)
    serializer =BookSerializer(book)
    return Response(serializer.data)
@api_view(['POST'])
def api_register(request):
    username=request.data.get('username')
    password =request.data.get('password')
    email=request.POST.get('email')
    if User.objects.filter(username=username).exists():
             return Response({request,"Username already exists"},status=status.HTTP_400_BAD_REQUESTS)
            
    user=User.objects.create_user(
            username=username,
            email=email,
            password=password
            )
    return Response({'message': 'User Created Successfully'},status=status.HTTP_201_OCREATED)
@api_view(['POST'])
def api_login(request):
    username=request.data.get('username')
    password =request.data.get('password')
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return Response({'message':'Login successful'},status=status.HTTP_200_Ok)
    else:
         return Response({'error':'invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'message':'Logout successful'},status=status.HTTP_200_Ok)
    else:
        return Response({'error':'User not logged in'},status=status.HTTP_400_BAD_REQUEST)
