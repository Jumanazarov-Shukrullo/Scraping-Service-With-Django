import datetime as dt

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserCreationForm, UserUpdateForm, ContactForm
from scraping.models import Error

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        messages.success(request, 'Registered new user')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Saved successfully')
                return redirect('update')
        else:
            form = UserUpdateForm(
                initial={'city': user.city, 'language': user.language,
                         'send_email': user.send_email}
            )
            return render(request, 'accounts/update.html',
                          {'form': form, 'contact_form': contact_form})
    else:
        return redirect('login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'User is deleted')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data')
                data.append({'city': city, 'language': language, 'email': email})
                data['user_data'] = data
                err.save()
            else:
                data = [{"city": city, "language": language, "email": email}]
                Error(data=f'user_data: {data}').save()
            messages.success(request, 'Form is sent to admin')
            return redirect('update')
        else:
            return redirect('update')
    else:
        return redirect('login')
