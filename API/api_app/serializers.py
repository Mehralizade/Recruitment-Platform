from rest_framework import serializers

from models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Subject
        fields = ('__all__')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = ('__all__')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research_Announcement
        fields = ('__all__')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('__all__')