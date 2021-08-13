from django.db import models
from django.contrib import auth
from django.utils import timezone
# Create your models here.

class Study_Subject(auth.models.User, auth.models.PermissionsMixin):
    Male = 'M'
    Female = 'F'
    Other = 'O'
    Not_Disclosed = 'N'
    Gender_Choices = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other'),
        (Not_Disclosed, 'Not disclosed'),
        
    ]
    gender = models.CharField(
        max_length=2,
        choices=Gender_Choices,
        default=Not_Disclosed,
    )
    is_researcher = models.BooleanField()
    bank_account = models.TextField()
    age = models.PositiveIntegerField()
    def __str__(self):
        return "@{}".format(self.username)

class Researcher(auth.models.User, auth.models.PermissionsMixin):
    is_researcher = models.BooleanField()

    def __str__(self):
        return "@{}".format(self.username)

class Research_Announcement(models.Model):
    Online = 'On'
    Offline = 'Off'
    Setting = [
        (Online, 'Online'),
        (Offline, 'Offline'),
        
    ]
    setting = models.CharField(
        max_length=4,
        choices=Setting,
        default=Online,
    )
    author = models.ForeignKey(Researcher,on_delete=models.CASCADE,null=True,related_name='my_posts')
    title = models.CharField(max_length=400)
    description = models.TextField()
    exp_type = models.CharField(max_length=400)
    collected_data = models.TextField()
    reward = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    participant_number = models.PositiveIntegerField()
    date = models.DateTimeField()
    location = models.CharField(max_length=1000)
    additional_info = models.TextField()
    #exp_image = models.ImageField(upload_to='announcement_images/',default='')
    #document1 = models.FileField(upload_to='announcement_files/')
    #document2 = models.FileField(upload_to='announcement_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Study_Subject, related_name='likes', blank=True)
    applicants = models.ManyToManyField(Study_Subject, related_name='my_applications', blank=True)
    confirmed_applicants = models.ManyToManyField(Study_Subject, related_name='confirmend_applications', blank=True)
    declined_applicants = models.ManyToManyField(Study_Subject, related_name='declined_applications', blank=True)
    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
    def total_applicants(self):
        return self.applicants.count()
    def confirment(self):
        return self.confirmed_applicants.count()
    def declined(self):
        return self.declined_applicants.count()

class Rating(models.Model):
    rated = models.ForeignKey(Study_Subject,on_delete=models.CASCADE,null=True,related_name='my_ratings')
    rater = models.ForeignKey(Researcher,on_delete=models.CASCADE,null=True,related_name='rated_applicants')
    criteria1 = models.PositiveIntegerField()
    criteria2 = models.PositiveIntegerField()
    criteria3 = models.PositiveIntegerField() 
    overall_rating = models.PositiveIntegerField()