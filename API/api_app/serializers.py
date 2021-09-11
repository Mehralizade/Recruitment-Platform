from rest_framework import serializers
from rest_framework.authtoken.views import Token

from .models import *

class StudySubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Subject
        fields = ('username', 'password','is_researcher', 'gender', 'age', 'bank_account')

        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
        }}

    def create(self, validated_data):
        study_subject = Study_Subject.objects.create_user(**validated_data)
        Token.objects.create(user=study_subject)
        return study_subject

class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = ('username', 'password','is_researcher',)

        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
        }}

    def create(self, validated_data):
        researcher = Researcher.objects.create_user(**validated_data)
        Token.objects.create(user=researcher)
        return researcher
       

class ResearchAnnouncementSerializer(serializers.ModelSerializer):

    
    
    class Meta:
        model = Research_Announcement
        fields = ('__all__')

        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('__all__')

       