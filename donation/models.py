from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=250)


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
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

