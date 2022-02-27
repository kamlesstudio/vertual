from django.db import models
from django.urls import reverse
# Create your models here.
from django.contrib.auth.models import User
from datetime import date

import uuid

class Profile(models.Model):
    SELECT_OPTIONS = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True , blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=500,null=True,blank=True,unique=True)
    username = models.CharField(max_length=200,null=True,blank=True,unique=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    pin_number = models.CharField(max_length=2000,null=True,blank=True)
    mobile_no = models.CharField(max_length=200,null=True,blank=True)
    language = models.CharField(max_length=500,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    profile_image = models.FileField(null=True,blank=True, upload_to = 'profiles/',default = 'profiles/user-default.png')
    social_facebook = models.CharField(max_length=200,null=True,blank=True, help_text = "Please use the following format: https://")
    social_twitter = models.CharField(max_length=200,null=True,blank=True,help_text = "Please use the following format: https://")
    social_youtube = models.CharField(max_length=200,null=True,blank=True,help_text = "Please use the following format: https://")
    state = models.CharField(max_length=200,null=True,blank=True)
    social_website = models.CharField(max_length=200,null=True,blank=True,help_text = "Please use the following format: https://")
    open_time = models.CharField(max_length=200,null=True,blank=True,default=0)
    closed_time = models.CharField(max_length=200,null=True,blank=True,default=0)
    publish = models.BooleanField(default=0)
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    percentage = models.CharField(max_length=50,default=0,null=True,blank=True)
    check = models.BooleanField(default=1)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)
    shop_name = models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    latitude = models.CharField(max_length=2000,null=True,blank=True)
    longitude = models.CharField(max_length=2000,null=True,blank=True)
    note = models.CharField(max_length=500,null=True,blank=True,default=None)
    select_opt = models.CharField(max_length=60,default=None,blank=True ,null=True ,choices=SELECT_OPTIONS)


    def __str__(self):
        return str(self.username)
     
    def get_absolute_url(self):
         return reverse('user-profile', args=[str(self.id)])
    @property
    def get_photo_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
            
    def number_of_likes(self):
            return self.likes.count()

    @property
    def get_photo_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
    
    
class Skill(models.Model):
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    recipient = models.ManyToManyField(Profile,blank=True,related_name='messages')
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField()
    pin_number = models.CharField(max_length=2000,null=True,blank=True)
    is_read = models.BooleanField(default=False,null =True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)
    banner_image = models.ImageField(null=True,blank=True, upload_to = 'profiles/',default = 'profiles/user-default.png')

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ['is_read','-created']


class Reviewprofile(models.Model):
    VOTE_TYPE =(
        ('up','up Vote'),
        ('down','Down Vote'),
    )
    votee =models.ForeignKey(Profile,models.CASCADE,null=True)
    value = models.CharField(max_length = 200,choices=VOTE_TYPE)
    voting = models.ManyToManyField(Profile,blank=True,related_name="profile_likes")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

   

    def __str__(self):
        return f'%s ,%s'%(self.value,self.votee.name)
    