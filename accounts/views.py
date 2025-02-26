from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterModelForm, UserLoginForm, UserProfileForm, ForgotPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .service import send_email_alternative
from .models import Code
from django.utils import timezone

from django_ratelimit.decorators import ratelimit
# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('posts')
            else:
                form.add_error(None, 'password or username is incorrect.')
                return render(request, 'login.html', {'forms': form})
            #v1
            # user = User.objects.filter(username=username).first()
            # if user and user.check_password(password):
            #     pass

    form = UserLoginForm()
    data = {
        'forms': form
    }
    return render(request, 'login.html', context=data)

def register(request):
    if request.method == 'POST':
        form = UserRegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('posts')
        return render(request, 'register.html', {'forms': form})


    form = UserRegisterModelForm()
    data = {
        'forms': form
    }
    return render(request, 'register.html', context=data)

@login_required
def logout_user(request):
    print(request.user)
    logout(request)
    return redirect('posts')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('accounts:profile')
        # form.add_error('Some fields are invalid.')

    data = {
        'forms': form
    }

    return render(request, 'profile_edit.html', data)

@ratelimit(key='ip', rate='10/m', block=True)
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            send_email_alternative(email, user)
            request.session['reset_email'] = email

            return render(request, 'check_email.html')

    form = ForgotPasswordForm()
    data = {
        'forms': form
    }
    return render(request, 'reset_password.html', data)

@ratelimit(key='ip', rate='6/m', block=True)
def verify_code(request):
    if request.method == 'POST':
        passcode = request.POST.get('verification_code')

        email = request.session.get('reset_email')
        if not email:
            return redirect('accounts:forgot_password')
        user = User.objects.filter(email=email).first()
        if not user:
            print('User not found')
            return redirect('accounts:forgot_password')

        code = Code.objects.filter(user=user).first()
        if not code:
            print('code doesn\'t exists')
            return redirect('accounts:forgot_password')
        print(f"{code.expire_date=}, {timezone.now()=}")
        if code.expire_date < timezone.now():
            print('code is expired')
            return render(request, 'check_email.html')

        if code.code_number != passcode:
            print('code doesn\'t match')
            return render(request, 'check_email.html')

        request.session['reset_email'] = email
        code.delete()
        return render(request, 'create_new_password.html')



    return render(request, 'check_email.html')

@ratelimit(key='ip', rate='5/m', block=True)
def create_new_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session['reset_email']
        user = User.objects.filter(email=email).first()
        if not user:
            print('User doesn\'t exists.')
            return redirect('home')

        if password != confirm_password:
            print('Passwords don\'t match.')
        user.set_password(password)
        user.save()
        try:
            del request.session['reset_email']
        except Exception as e:
            print(f"e")
        return redirect('accounts:login')

    return redirect('accounts:login')