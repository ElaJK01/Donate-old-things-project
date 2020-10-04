from donation.models import Institution, Category, Donation
from rest_framework import serializers


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('name', 'description', 'type', 'categories')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ('quantity', 'categories', 'institution', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date',
                  'pick_up_time', 'pick_up_comment', 'user')
