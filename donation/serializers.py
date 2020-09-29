from donation.models import Institution, Category
from rest_framework import serializers


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ('name', 'description', 'type', 'categories')


class CategorySerializer(serializers.ModelSerializer):
    class meta:
        model = Category
        fields = ('name')

