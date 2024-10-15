from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
#from django import forms

def search(request):
  #Determine if the form has been filled
  if request.method == "POST":
      searched = request.POST['searched']
      return render(request, "search.html", {'searched':searched})
  else:
    return render(request, "search.html", {})

def update_info(request):
  if request.user.is_authenticated:
    current_user = Profile.objects.get(user__id=request.user.id)
    form = UserInfoForm(request.POST or None, instance=current_user)
    if form.is_valid():
      form.save()
      messages.success(request, "Your info has been updated")
      return redirect('home')
    
    return render(request, 'update_info.html', {'form':form})
  else:
    messages.success(request, "You must be logged in to access this page!!!")
  return redirect('home')
# def update_password(request):
#   if request.user.is_authenticated:
#       current_user = request.user
#       if request.method == 'POST':
#       #DO STUFFd
#        else:
#         form = ChangePasswordForm(current_user)
#         return render(request, 'update_password.html', {'form':form})
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
              form.save()
              messages.success(request, "Your password has been updated....")
              login(request, current_user)
              return redirect('update_user')
            else:
              for error in list(form.errors.values()):
                messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
      messages.success(request, "You must be logged in to access this page")

def update_user(request):
  if request.user.is_authenticated:
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    if user_form.is_valid():
      user_form.save()
      
      login(request, current_user)
      messages.success(request, "User has been updated")
      return redirect('home')
    
    return render(request, 'update_user.html', {'user_form':user_form})
  else:
    messages.success(request, "You must be logged in to access this page")
  return redirect('home')

def category_summary(request):
  categories = Category.objects.all()
  return render(request, 'category_summary.html', {'categories':categories})

def category(request,foo):
  foo = foo.replace('-', '/')
  try:
    category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products':products, 'category':category})
  except:
    messages.success(request, ("There was an error trying to get the category page"))
    return redirect('home')

def product(request,pk):
  product = Product.objects.get(id=pk)
  return render(request, 'product.html', {'product':product})



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
      messages.success(request, ("Username Created, Please Fill Out The Form Below..."))
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

def register_user(request):
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      # log in uaser
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, ("Username Created, Please Fill Out The Form Below..."))
      return redirect('update_info')
    else:
      messages.success(request, ("There was a problem trying to register you, please try again "))
      return redirect('register')
  else:
    return render(request, 'register.html', {'form':form})
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import SignUpForm

# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the form and get the user object
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')  # Get the raw password
#             # log in the user
#             user = authenticate(username=username, password=raw_password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "You have successfully registered your account")
#                 return redirect('home')
#         else:
#             messages.error(request, "There was a problem trying to register you, please try again.")
#     else:
#         form = SignUpForm()

#     return render(request, 'register.html', {'form': form})
