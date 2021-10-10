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

class UsersViewSet(viewsets.ModelViewSet):
     def get_queryset(self):
        queryset = Researcher.objects.all()
        search_param1 = self.request.query_params.get('username', None)
        if  Researcher.objects.filter(username=search_param1).exists():
            return Researcher.objects.filter(username=search_param1)
        else:
            return Study_Subject.objects.filter(username=search_param1)
        
class AnnouncementPostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing research announcements.
    """
    def get_queryset(self):
        queryset = Research_Announcement.objects.all()
        search_param1 = self.request.query_params.get('date', None)
        search_param2 = self.request.query_params.get('reward', None)
        search_param3 = self.request.query_params.get('setting', None)
        search_param4 = self.request.query_params.get('researcher_id', None)
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
        
        if search_param4 is not None:
            queryset = Research_Announcement.objects.filter(author=search_param4)


            
       
           
        return queryset
    serializer_class = ResearchAnnouncementSerializer

class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing research announcements.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serializer_class = ResearcherSerializer
        if Researcher.objects.filter(username=user.username).exists():
            response =  Researcher.objects.filter(username=user.username)
        else:
            serializer_class = StudySubjectSerializer
            response =  Study_Subject.objects.filter(username=user.username)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username':user.username,
            
            'is_researcher':response.values_list('is_researcher', flat=True).order_by('id')[0]
        })