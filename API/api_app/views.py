from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
import datetime
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
    def get_queryset(self):
        queryset = Research_Announcement.objects.all()
        search_param1 = self.request.query_params.get('date', None)
        search_param2 = self.request.query_params.get('reward', None)
        search_param3 = self.request.query_params.get('setting', None)

        if search_param1 is not None:
            if search_param1=='three':
                queryset = Research_Announcement.objects.all().filter(date__range=(datetime.date.today()-datetime.timedelta(days=1), 
                datetime.date.today()))
            
            elif search_param1=='One week':
                queryset = Research_Announcement.objects.all().filter(created_at__range=(datetime.date.today(), 
                datetime.date.today()+datetime.timedelta(days=7)))

        if search_param2 is not None:
            if search_param3 is not None:
                if search_param2=='Ascending' and search_param3=='Online':
                    queryset = Research_Announcement.objects.all().order_by('reward').filter(setting='On')
                elif search_param2=='Descending' and search_param3=='Online':
                    queryset = Research_Announcement.objects.all().order_by('-reward').filter(setting='On')
                elif search_param2=='Descending' and search_param3=='All':
                    queryset = Research_Announcement.objects.all().order_by('-reward')
                elif search_param2=='Ascending' and search_param3=='All':
                    queryset = Research_Announcement.objects.all().order_by('reward')
            elif search_param2=='Ascending':
                queryset = Research_Announcement.objects.all().order_by('reward')
            else:
                queryset = Research_Announcement.objects.all().order_by('-reward')
        
                


            
       
           
        return queryset
    serializer_class = ResearchAnnouncementSerializer

class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing research announcements.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


