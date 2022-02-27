from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill,Message
from .models import Reviewprofile
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','password1','password2']
        labels = {
            'first_name':'Name',
        }

    def clean_email(self):
            # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username','mobile_no','select_opt','bio','location','shop_name','address','state','pin_number','language','profile_image','open_time','closed_time','note','social_facebook','social_twitter','social_youtube','social_website','publish','check']
        labels = {
            'publish':'Do you want to public your profile',
            'check':'Turn On or Off when you available',
            'note':'Important note in profile',
            'select_opt':'Please choose option to hide/show your number',
        }
        widgets = {

            'name': forms.TextInput(attrs={'placeholder': 'full name'}),
            'social_facebook': forms.TextInput(attrs={'placeholder':'Please use the following format: https://'}),
            'social_twitter': forms.TextInput(attrs={'placeholder':'Please use the following format: https://'}),
            'social_youtube': forms.TextInput(attrs={'placeholder':'Please use the following format: https://'}),
            'pin_number': forms.TextInput(attrs={'placeholder':'Please fill area pin code'}),
            'select_opt':forms.RadioSelect()

        }
    def __init__(self,*args,**kwargs):
        super( ProfileForm,self).__init__(*args,**kwargs)
        self.fields['pin_number'].required = True

            #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

    def pin_number_clean(self):
        pin_number = self.cleaned_data.get('pin_number')
        if not pin_number:
            raise forms.ValidationError('This field is required')
        return pin_number

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of Skill'}),
            'description': forms.Textarea(attrs={'placeholder': 'Basic information about skill'}),
        }
    def __init__(self,*args,**kwargs):
        super( SkillForm,self).__init__(*args,**kwargs)

            #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body','pin_number','banner_image']
        widgets = {

            'name': forms.TextInput(attrs={'placeholder': 'Name of Sender'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email of Sender'}),
            'pin_number': forms.TextInput(attrs={'placeholder': 'recipients pin number'}),

        }
    def __init__(self,*args,**kwargs):
        super( MessageForm,self).__init__(*args,**kwargs)

            #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewprofileForm(ModelForm):
    class Meta:
        model = Reviewprofile
        fields = ['value']
        labels={
            'value':'place your vote',
        }
    def __init__(self,*args,**kwargs):
        super(ReviewprofileForm,self).__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})