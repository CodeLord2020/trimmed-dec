from django.shortcuts import render, redirect
import os
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib import messages

from .forms import MyUserCreationForm


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['repeat_password']
         
        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'E-mail already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,email = email, password  = password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matched')
            return redirect('register')

    else:
        return render(request, 'auth/register.html')

def login(request):
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']

         user = auth.authenticate(username = username, password  = password)

         if user is not None:
            auth.login(request, user)
            return redirect('home')

         else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'auth/login.html')

def logout(request):
    auth.logout(request)
    return redirect('landing')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            subject = 'Reset Password Request:'
            reset_link = request.build_absolute_uri('/') + f'reset_password/{uid}/{token}/'
            message = f'Click on the link to reset your password: {reset_link}'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [email], fail_silently=False)
            messages.success(request, 'An email has been sent to reset your password')
            return redirect ('auth/login')
        else:
            messages.error(request, 'No user found with that email address')
    return render(request, 'auth/forgot_password.html')

def reset_password(request, uid, token):
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    # messages.success(request, 'Password reset successful')
                    return redirect('auth/login')
                else:
                    messages.error(request, 'Passwords do not match')
            return render(request, 'auth/reset_password.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    messages.error(request, 'Invalid or Expired link')
    return redirect('auth/forgot_password')
