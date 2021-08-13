from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets

# Create your views here.
class StudySubjectViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing study subject accounts.
    """
    queryset = Study_Subject.objects.all()
    serializer_class = StudySubjectSerializer


class ResearcherViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing researcher accounts.
    """
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer

class AnnouncementPostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing research announcements.
    """
    queryset = Research_Announcement.objects.all()
    serializer_class = ResearchAnnouncementSerializer

class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing research announcements.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


