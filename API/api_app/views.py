from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from datetime import datetime, timedelta
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
        queryset = Research_Announcement.objects.order_by('-created_at')
        print(queryset)
        search_param1 = self.request.query_params.get('date', None)
        search_param2 = self.request.query_params.get('reward', None)
        search_param3 = self.request.query_params.get('setting', None)
        search_param4 = self.request.query_params.get('researcher_id', None)
        search_param5 = self.request.query_params.get('applied', None)
        search_param6 = self.request.query_params.get('confirmed', None)
        search_param7 = self.request.query_params.get('declined', None)
        if search_param1 is not None:
            if search_param1=='3':
                three_days_ago = datetime.today() - timedelta(days=3)
                queryset = queryset.filter(created_at__gte=three_days_ago)
            
            elif search_param1=='7':
                one_week_ago = datetime.today() - timedelta(days=7)
                queryset = queryset.filter(created_at__gte=one_week_ago)

        if search_param2 is not None:
            if search_param3 is not None:
                if search_param2=='Ascending' and search_param3=='Online':
                    queryset = queryset.order_by('reward').filter(setting='On')
                elif search_param2=='Descending' and search_param3=='Online':
                    queryset = queryset.order_by('-reward').filter(setting='On')
                elif search_param2=='Descending' and search_param3=='All':
                    queryset = queryset.order_by('-reward')
                elif search_param2=='Ascending' and search_param3=='All':
                    queryset = queryset.order_by('reward')
            elif search_param2=='Ascending':
                queryset = queryset.order_by('reward')
            else:
                queryset = queryset.order_by('-reward')
        
        if search_param4 is not None:
            queryset = Research_Announcement.objects.filter(author=search_param4)
        if search_param5 is not None:
            queryset = Research_Announcement.objects.filter(applicants=search_param5)
        if search_param6 is not None:
            queryset = Research_Announcement.objects.filter(confirmed_applicants=search_param6)
        if search_param7 is not None:
            queryset = Research_Announcement.objects.filter(declined_applicants=search_param7)
        

        
       
           
        return queryset
    
        
    def partial_update(self, request, *args, **kwargs):
        post_object = self.get_object()
        data = request.data
        try:
            author = Researcher.objects.get(id=data["author"])
            post_object.author.add(author.id) 
        except KeyError:
            pass
        try:
            likes = Study_Subject.objects.get(id=data["likes"])
            post_object.likes.add(likes.id) 
        except KeyError:
            pass
        try:
            applicants = Study_Subject.objects.get(id=data["applicants"])
            post_object.applicants.add(applicants.id) 
        except KeyError:
            pass
        try:
            confirmed_applicants = Study_Subject.objects.get(id=data["confirmed_applicants"])
            post_object.confirmed_applicants.add(confirmed_applicants.id) 
        except KeyError:
            pass
        try:
            declined_applicants = Study_Subject.objects.get(id=data["declined_applicants"])
            post_object.declined_applicants.add(declined_applicants.id) 
        except KeyError:
            pass
        

        post_object.title = data.get("title", post_object.title)
        post_object.description = data.get("description", post_object.description)
        post_object.exp_type = data.get("exp_type", post_object.exp_type)
        post_object.collected_data = data.get("collected_data", post_object.collected_data)
        post_object.reward = data.get("reward", post_object.reward)
        post_object.duration = data.get("duration", post_object.duration)
        post_object.participant_number = data.get("participant_number", post_object.participant_number)
        post_object.date = data.get("date", post_object.date)
        post_object.time = data.get("time", post_object.time)
        post_object.location = data.get("location", post_object.location)
        post_object.additional_info = data.get("additional_info", post_object.additional_info)
        
        post_object.created_at = data.get("created_at", post_object.created_at)
        
        
        post_object.save()
        
        
        
        serializer = ResearchAnnouncementSerializer(post_object)

        return Response(serializer.data)
    serializer_class = ResearchAnnouncementSerializer

class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing research announcements.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        user = Study_Subject.objects.get(id=data["rated"])
        if user.reputation == None:
            user.reputation = data["overall_rating"]
        else:
            user.reputation = (user.reputation+data["overall_rating"])//2
        
        user.save()
        print(user.reputation)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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



