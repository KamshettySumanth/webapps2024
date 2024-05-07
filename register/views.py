from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from register.models import CustomUser
from .forms import SignupForm
from django.db.models import Q

def signin(request):
    """ 
    Handles user sign-in.

    If the user is already authenticated, it redirects them to the home.
    
    If the request method is POST, it attempts to authenticate the user with the provided 
    identifier (email or username) and password. If authentication is successful, the user 
    is logged in and redirected to the home. Otherwise, an error message is displayed 
    indicating invalid credentials.

    Exceptions related to user existence are caught and handled by displaying a specific 
    error message.

    Returns:
        If the user is authenticated, redirects to the home.
        If the authentication fails or the request method is not POST, renders the login 
        template.
    """
    try:
        if request.user.is_authenticated:
            return redirect('home')
        if request.method == 'POST':
            identifier = request.POST.get('identifier')
            password = request.POST.get('password')
            if identifier and password:
                user = CustomUser.objects.filter(
                    Q(email=identifier) | Q(username=identifier)).first()
                if user:
                    email = user.email
                else:
                    messages.error(request, 'User does not exist')
                    return render(request, 'register/signin.html')
            
            if identifier and password:
                user = authenticate(request, 
                                    email=email,
                                    password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist')
    
    return render(request, 'register/signin.html')

def signup(request):
    """
    Handles registration view

    If the user is already authenticated, it redirects them to the home.

    If the request method is POST, it creates a new registration form with the submitted data
    and validates it. If the form is valid, it saves the user and redirects to the login page.
    Otherwise, it renders the registration template with the form.
    
    """

    if request.user.is_authenticated:
        return redirect('home')
    register_form = SignupForm()
    if request.method == 'POST':
        try:
            register_form = SignupForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(
                    request, 'Your account has been activated successfully')
                return redirect('signin')
            else:
                messages.error(request, 'Either username or email already exists.')
                return redirect('signup')
        except Exception as e:
            messages.error(request, e)
    context = {
        'register_form': register_form,
        'forms': [register_form,]
    }
    return render(request, 'register/signup.html', context)


@login_required(login_url='signin')
def admins(request):
    if request.user.is_superuser:
        admins = CustomUser.objects.filter(is_superuser=True)
    else:
        messages.error(request, 'Unauthorized access. You cannot access this page')
        return redirect('login')
    context = {
        'admins': admins
        }
    return render(request, 'register/all-admins.html', context)


@login_required(login_url='signin')
def add_admin(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Unauthorized access')
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.save()
            messages.success(request, 'Admin added successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = SignupForm()
        
    return render(request, 'register/add-admin.html', {'form': form})


@login_required(login_url='signin')
def delete_admin(request, user):
    if request.user.is_superuser:
        admin = get_object_or_404(CustomUser, id=user)
        if admin == request.user:
            messages.error(request, "You can't delete yourself")
            return redirect('admins')
        if admin:
            admin.delete()
            messages.success(request, "Admin delete successfully")
            return redirect('admins')
    else:
        messages.error(request, 'Access denied. Unauthorized access')
    return render(request, 'register/admins.html')


@login_required(login_url='signin')
def logout(request):
    auth_logout(request)
    messages.success(request, 'Signed out successfully')
    return redirect('signin')

