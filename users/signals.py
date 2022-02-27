

from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):
    print('hi')
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )

@receiver(post_save,sender=Profile)
def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


        subject ='Welcome to VIRTUAL BAZAR'
        message = 'Thanks for registering here'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
    )

@receiver(post_delete,sender=Profile)
def deleteUser(sender,instance,**kwargs):
    print(sender)
    print(instance)
    user = instance.user
    user.delete()

# post_save.connect(profileUpdated,sender=Profile)
# post_delete.connect(deleteUser,sender=Profile)