from django.db import models
from django.forms import ModelForm, fields
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields =['title','featured_image','featured_image_1','featured_image_2','featured_image_3','description','add_note','check','demo_link','source_link','tags','price']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'placeholder': 'Name of Product/service'}),
            'description': forms.Textarea(attrs={'placeholder': 'Basic information about product/service'}),
            'add_note': forms.TextInput(attrs={'placeholder': 'product/service price concession'}),
        }
        
        labels = {
            'check': 'Availability'
              
        }

    def __init__(self,*args,**kwargs):
       
        super(ProjectForm,self).__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels={
            'value':'place your vote',
            'body':'Add your comment with your vote'
        }
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
