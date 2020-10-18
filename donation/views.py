from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from donation.forms import RegisterForm, DonationForm
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




# class Donations(ListAPIView):
#     serializer_class = DonationSerializer
#     queryset = Donation.objects.all()
#
#
# class DonationAdd(CreateAPIView):
#     serializer_class = DonationSerializer
#     queryset = Donation.objects.all()


class Institutions(ListAPIView):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        print(category_id)
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
    def get(self, request):
        user = self.request.user
        ctx ={'user': user}
        return render(request, 'profil.html', ctx)

