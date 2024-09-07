from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
  products = Product.objects.all()
  return render(request, 'home.html', {'products':products})

def about(request):
  return render(request, 'about.html', {})

def login_user(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, ("You have been successfully logged in."))
      return redirect('home')
    else:
        messages.success(request, ("There was an error trying to log you in please try again"))
        return redirect('login')
  else:
    return render(request, 'login.html')
  
  
  
  
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from django.shortcuts import render, redirect

# def login_user(request):
#     if request.method == "POST":
#         # Use .get() to avoid MultiValueDictKeyError
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         if username and password:  # Check if both fields are filled
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "You have been successfully logged in.")
#                 return redirect('home')
#             else:
#                 messages.error(request, "There was an error trying to log you in, please try again.")
#                 return redirect('login')
#         else:
#             messages.error(request, "Please enter both username and password.")
#             return redirect('login')
#     else:
#         return render(request, 'login.html')


def logout_user(request):
  logout(request)
  messages.success(request, ("You have been logged out, thank you for stopping by!!"))
  return redirect('home')
