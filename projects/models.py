from django.db import models
import uuid
from django.utils import timezone

from datetime import date
from django.urls import reverse
from users.models import Profile
# Create your models here.
from django.core.validators import MaxValueValidator,MinValueValidator


class Project(models.Model):
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length = 200)
    description = models.TextField(null=True,blank=True)

    featured_image = models.FileField(null=True,
                                        blank=True,default='default.jpg')
    
    featured_image_1 = models.FileField(null=True,
                                        blank=True,default='default.jpg')
                                        
    featured_image_2 = models.FileField(null=True,
                                        blank=True,default='default.jpg')
                                        
    featured_image_3 = models.FileField(null=True,
                                        blank=True,default='default.jpg')
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True,blank=True,default=timezone.now)
    tags = models.ManyToManyField('Tag',blank=True)
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    percentage = models.CharField(max_length=50,default=0,null=True,blank=True)
    price = models.CharField(max_length=200,null=True,blank=True,default=0)
    count = models.IntegerField(null=True,blank=True,default=0)
    add_note = models.CharField(max_length=2000,null=True,blank=True)
    liked = models.ManyToManyField(Profile,blank=True,default=None,related_name="project_likes")
    check = models.BooleanField(default=1)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

    def __str__(self):
        return self.title
    @property
    def num_likes(self):
        return self.liked.all().count()
   

    class Meta:
        ordering =['count']



class Review(models.Model):
    VOTE_TYPE =(
        ('up','up Vote'),
        ('down','Down Vote'),
    )
    owner =models.ForeignKey(Profile,models.CASCADE,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length = 200,choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

    class Meta:
        unique_together =[['owner','project']]
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

    
    def __str__(self):
        return self.name


LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)

    def __str__(self):
        return str(self.project)

     