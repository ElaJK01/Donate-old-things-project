from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from donation.forms import RegisterForm
from django.contrib.auth.models import User
from donation.models import CustomUser, Category, Institution
from django.contrib.auth.mixins import LoginRequiredMixin



class LandingPage(View):
    def get(self, request):
        return render(request, 'index.html')


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {'categories': categories,
               'institutions': institutions}
        return render(request, 'form.html', ctx)

    def post(self, request):
        ...


class Login(LoginView):
    def form_invalid(self, form):
        return redirect('register')


class Register(View):
    def get(self, request):
        form = RegisterForm()
        ctx = {'form': form}
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                new_user = CustomUser.objects.create_user(email=email, name=name, last_name=last_name)
                new_user.set_password(password)
                new_user.save()
                return redirect('login')
        else:
            ctx = {'msg': "Niepoprawnie wypełniony formularz!"}
            return render(reqest, 'register.html', ctx)

