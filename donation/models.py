from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email'), unique=True)
    name = models.CharField(max_length=250, verbose_name='Imię')
    last_name = models.CharField(max_length=250, verbose_name='Nazwisko')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Institution(models.Model):
    FUNDATION = 1
    NGO = 2
    LOCAL_COLLECTION = 3

    TO_WHO_DONNATE = (
        (FUNDATION, 'Fundation'),
        (NGO, 'NGO'),
        (LOCAL_COLLECTION, 'Local collecion'),
    )
    name = models.CharField(max_length=250)
    description = models.TextField()
    type = models.IntegerField(choices=TO_WHO_DONNATE, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=250)
    phone_number = PhoneField(blank=True, help_text='Telefon kontaktowy')
    city = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=250)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)







