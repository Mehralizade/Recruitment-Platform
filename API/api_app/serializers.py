from rest_framework import serializers

from .models import *

class StudySubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Subject
        fields = ('__all__')

class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = ('__all__')


class ResearchAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research_Announcement
        fields = ('__all__')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('__all__')