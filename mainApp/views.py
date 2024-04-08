from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SignUpForm ,ChangePasswordForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def index(request):
    return render(request, 'index.html')



# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registration successful. You can now login.')
#             return redirect('login')  
#     else:
#         form = SignUpForm()
#     return render(request, 'register.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'noreply@socialdjango.azurewebsites.net', [to_email])

            return render(request, 'registration_success.html')  
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def verify_email(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.is_active:
        messages.error(request, 'Email already verified.')
    else:
        user.is_active = True
        user.save()
        messages.success(request, 'Email verified successfully. You can now log in.')
    return redirect('login')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('dashboard')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, ChangePasswordForm
from .models import Profile

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')

    else:
        profile_form = ProfileForm(instance=profile)

    context = {'profile_form': profile_form}
    return render(request, 'profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.POST)
        if password_form.is_valid():
            user = request.user
            old_password = password_form.cleaned_data['old_password']
            new_password1 = password_form.cleaned_data['new_password1']
            new_password2 = password_form.cleaned_data['new_password2']
            if user.check_password(old_password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('profile')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Incorrect old password.')
    else:
        password_form = ChangePasswordForm()
    
    return render(request, 'change_password.html', {'password_form': password_form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
