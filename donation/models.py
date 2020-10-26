from django.db import models
from phone_field import PhoneField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


class MyUserManager(BaseUserManager):

    def create_user(self, email, name, last_name, password=None):

        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, last_name, password=None):

        user = self.create_user(
            email,
            name=name,
            last_name=last_name,
            password=password
            )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=250, verbose_name='Imię')
    last_name = models.CharField(max_length=250, verbose_name='Nazwisko')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    objects = MyUserManager()

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


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
    user = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address}, {self.pick_up_time}'





