from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from donation.forms import RegisterForm, DonationForm, UpdateUserForm
from donation.models import MyUser, Category, Institution, Donation
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InstitutionSerializer, DonationSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages



class LandingPage(View):
    def get(self, request):
        institutions_number = Institution.objects.all().count()
        institutions = Institution.objects.all()
        bags_number = Donation.objects.aggregate(Sum('quantity'))
        bags_number = bags_number['quantity__sum']
        categories = Category.objects.all()
        fundations = Institution.objects.filter(type=1)
        ngos = Institution.objects.filter(type=2)
        collections = Institution.objects.filter(type=3)
        ctx = {'institutions_number': institutions_number,
               'institutions': institutions,
               'bags_number': bags_number,
               'categories': categories,
               'fundations': fundations,
               'ngos': ngos,
               'collections': collections}
        return render(request, 'index.html', ctx)


class Confirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):
        form = DonationForm()
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {'categories': categories,
               'institutions': institutions,
               'form': form}
        return render(request, 'form.html', ctx)

    def post(self, request):
        if self.request.is_ajax() and self.request.method == "POST":
            form = DonationForm(request.POST)
            if form.is_valid():
                user = self.request.user
                categories = form.cleaned_data['categories']
                bags = form.cleaned_data['quantity']
                institution = form.cleaned_data['institution']
                address = form.cleaned_data['address']
                city = form.cleaned_data['city']
                postcode = form.cleaned_data['postcode']
                phone = form.cleaned_data['phone']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                comments = form.cleaned_data['comments']

                donation = Donation.objects.create(quantity=bags, institution=institution, address=address,
                                                  phone_number=phone, city=city, zip_code=postcode, pick_up_date=date,
                                                   pick_up_time=time, pick_up_comment=comments, user=user)
                donation.categories.set(categories)
                donation.save()
                ser_donation = serializers.serialize('json', [donation, ])

                return JsonResponse({"donation": ser_donation}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        else:
            JsonResponse({"error": ""}, status=400)


class Institutions(ListAPIView):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(categories__pk__in=[category_id])
        return queryset


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
                new_user = MyUser.objects.create_user(email=email, name=name, last_name=last_name)
                new_user.set_password(password)
                new_user.save()
                return redirect('login')
        else:
            ctx = {'msg': "Niepoprawnie wypełniony formularz!"}
            return render(reqest, 'register.html', ctx)


class Profil(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):
        user = self.request.user
        user_donations = Donation.objects.filter(user=user)
        if user_donations is None:
            msg = {'message': 'Nie przekazałeś jeszcze żadnych darów',
                   'user': user}
            return render(request, 'profil.html', msg)
        else:
            ctx ={'user': user,
                  'donations': user_donations}
            return render(request, 'profil.html', ctx)


class ProfileIsTaken(LoginRequiredMixin, View):

    """Enable confirm pick-up of donations"""
    login_url = 'login'

    def post(self, request):
        confirmation = request.POST.get('confirm')
        donation = get_object_or_404(Donation, pk=confirmation)
        if request.user.id == donation.user.id:
            donation.is_taken = True
            donation.save()
            return redirect('profil')

        else:
            ctx = {'ctx': 'Nie udało sie potwierdzić odbioru daru'}
            return render(request, 'profil.html', ctx)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """Enable to user to update data like name, surname and email"""

    login_url = 'login'
    form_class = UpdateUserForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('profil')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        ctx = {'form': form}
        return render(request, 'password.html', ctx)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Twoje hasło zostało zmienione!')
            return redirect('change_password')
        else:
            messages.error(request, 'Proszę popraw błędy')
            return render(request, 'password.html', {'form': form})


class PasswordUpdatedView(View):
    def get(self, request):
        return render(request, 'change_password.html')


