from genericpath import exists
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls.base import reverse
import re
from payments.utils import VerifyPaytmResponse
from projects.forms import ReviewForm
from .models import Profile, Reviewprofile ,Skill,Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CustomUserCreationForm, ProfileForm, SkillForm,MessageForm,ReviewprofileForm
from .utils import searchProfiles, paginateProfiles
from .models import Message
from projects.models import Project

from django.core.mail import send_mail
import math, random
# Create your views here.
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
                messages.error(request,'User Does Not Exists')
        print(email)
        print(password)
        v=request.session['useremail'] = email
        print(v)

        try:
            user = User.objects.get(email=email)
            print(user)
            user = authenticate(request,username=user,password=password)
            print(user)

            if user is not None:
                login(request,user)
                return redirect('account')
            else:
                messages.error(request,'Email or password is incoreect')
        except:
            messages.error(request,'Email does not exist')
    return render(request,'users/login_register.html')




def logoutUser(request):
    logout(request)
    messages.info(request,'user was logout')
    return redirect('projects')



def registerUser(request):
    print(request.POST)
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email#user.username.lower()
            user.save()

            messages.success(request,'User Account is created!')
            login(request,user)
            return redirect('edit-account')
        else:
             messages.error(request,'An error occurred during registration')

    context = {'page':page,'form':form}
    return render(request,'users/login_register.html',context)



def profiles(request):
  
    profiles ,search_query,search_query1 = searchProfiles(request)
    custom_range , profiles = paginateProfiles(request,profiles,5000)
    context = {'profiles':profiles,' search_query': search_query,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)


def reviewProfile(request,pk):
    print(request.POST)
    form = ReviewprofileForm()
    profile = Profile.objects.get(id=pk)
    user = request.user.profile
    ups = Reviewprofile.objects.filter(value='up')
    print(ups)
    reviewaccount = Reviewprofile()
    if request.method == "POST" and profile!=request.user.profile:
        vote = request.POST['value']
        
        # voter = Reviewprofile.objects.filter(voting=user)
        # print(voter)
        try:
            review_id = get_object_or_404(Reviewprofile,votee=profile,voting=user)
            voter=get_object_or_404(Reviewprofile,pk=review_id.id)
          
        except:
             
            reviewaccount.votee = profile
            reviewaccount.value = vote
            reviewaccount.save()
            reviewaccount.voting.add(user) 
            print('done')
        review_id = get_object_or_404(Reviewprofile,votee=profile,voting=user)
        voter=get_object_or_404(Reviewprofile,pk=review_id.id)
        if user in voter.voting.all() and voter.value==vote=='up':
           print('nothing to do')
           
        else:
            if user in voter.voting.all() and voter.value!=vote: 
                review_id = get_object_or_404(Reviewprofile,votee=profile,voting=user)
                print('id',review_id.id)
                voter.value = vote
                voter.save()
                print('added')
      
        u = Reviewprofile.objects.filter(id=review_id.id,value='up').count()
        
        d = Reviewprofile.objects.filter(id=review_id.id,value='down').count()
        s=profile.vote_total = u+d
       
        up = Reviewprofile.objects.filter(votee=profile,value='up').count()
        print('up',up)
        down = Reviewprofile.objects.filter(votee=profile,value='down').count()
        print('down',down)
        total = up+down
        
        try:
            profile.vote_ratio = up
            ratio = up/total
            profile.vote_total = total
            profile.percentage= str(ratio *100)
            profile.save()
        except ZeroDivisionError:
            ratio = 0
            profile.percentage= str(ratio *100)
            profile.save()
  
    context = {'form':form}
    return render(request,'users/user.html',context)

def userProfile(request,pk):
    print(request.POST)
    
    lst1=[]
    form = ReviewprofileForm()
    profile = Profile.objects.get(id=pk)
    publish = profile.publish
    projects = profile.project_set.all()
    
    inbox=[]
    try:
        inbox = Message.objects.filter(sender=profile).latest('created')
        print(lst1.append(inbox))
    except:
        pass
    print(projects)
    lst=[]
    if request.method == "POST" and request.POST.get('query') != None:
        search_query = request.POST.get('query')
        print(search_query)
        result = projects.filter(title__icontains = search_query)

        for item in result:
            dict = {}
            dict['id'] = item.id
            dict['title'] = item.title,
            print('dict',dict['title'])
            dict['owner'] = item.owner.name,
            dict['description'] = item.description,
            dict['image'] = item.featured_image.url,
            dict['price'] = item.price,
            dict['check'] = item.check,

            lst.append(dict)
            print(lst)
        return JsonResponse({'lst':lst})


    # lst =[]
    # if request.method == 'POST':
    #     for product in projects:
    #         lst.append(product.title.lower().split(" ")[0])
    #         print(lst)
    #         if search_query in lst:
    #             print(search_query)

        # product = projects.objects.filter(title__icontains = search_query)
        # print(product)
    print('pub',publish)
    page = request.GET.get('page', 1)
    paginator = Paginator(projects,2)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    try:
        vup = profile.vote_ratio 
        vt = profile.vote_total
        vp = profile.percentage
        print(vup,vt,vp)
    except:
        print('hi')
    context={
        'profile':profile,
        'topskills':topskills,
        'otherskills':otherskills,
        'publish':publish,
        'projects':projects,
        'result':lst,
        'form':form,
        'inbox':inbox,
        'lst1':lst1,
        'vt':vup,
        'vp':vp

    }
    return render(request,'users/user.html',context)

@login_required(login_url='login')
def userAccount(request):
    print(request.POST)
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    if request.method == 'POST':
        profile.latitude = request.POST.get('latitude')
        profile.longitude = request.POST.get('longitude')
        profile.save()

    # page = request.GET.get('page', 1)
    # paginator = Paginator(projects, 10)
    # try:
    #     projects = paginator.page(page)
    # except PageNotAnInteger:
    #     projects = paginator.page(1)
    # except EmptyPage:
    #     projects = paginator.page(paginator.num_pages)

    context={'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/ac.html',context)



@login_required(login_url='login')
def editAccount(request):
    print(request.POST)
    print(request.user)
    profile = request.user.profile
    print('pp',profile)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'skill added successfully!!')
            return redirect('account')
    context = {'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST,instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request,'skill updated successfully!!')
            return redirect('account')
    context = {'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'skill deleted successfully!!')
        return redirect('account')
    context={'object':skill}
    return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    print('msg',messageRequest)
    unreadCount= messageRequest.filter(is_read=False).count()
    inbox = Message.objects.filter(sender=profile)
    print(inbox)
    request.session['unreadcount']=unreadCount
    context={'messageRequest': messageRequest,'unreadCount':unreadCount,'inbox':inbox}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read =True
        message.save()
    context={'message':message }
    return render(request,'users/message.html',context)


@login_required(login_url='login')
def deleteMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    message.delete()
    messages.success(request,'message deleted successfully!!')
    return redirect("inbox")

@login_required(login_url='login')
def createMessage(request,pk):
    form=MessageForm()
    profile= request.user.profile
    pin = request.POST.get('pin_number')
    print(pin)
    recipient = Profile.objects.filter(pin_number=pin)
    count = Profile.objects.filter(pin_number=pin).count()
    print('recipient',recipient)
    sender = request.user.profile
    print(sender)
    print(request.POST)
    if request.method == 'POST':
        form=MessageForm(request.POST,request.FILES)
        if form.is_valid():
            message = form.save()

            for reciever in recipient:
                if reciever!=sender:
                    print(reciever)
                    message.sender = sender
                    message.name = sender.name
                    message.email = sender.email
                    reciever.messages.add(message)
                    message.save()
            message = f'Messages sent to  %s users successfully.' % count
            messages.success(request,message)
      #return redirect('account')

    context={'form':form}
    return render(request,'users/message_form.html',context)

def profileStatus(request):
    if request.is_ajax and request.user.is_authenticated:
        profile= request.user.profile
        pk = request.POST.get('profile_id')
        status = request.POST.get('state')
        print(request.POST)
        print(pk)
        print(status)

        if status=='true':
            status = True
            profile.check = status
            profile.save()
        if status=='false':
            status = False
            profile.check = status
            profile.save()

    return JsonResponse({'msg':'successful'})

def popupregisterUser(request):
    print(request.POST)
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        username = request.POST.get('username')

        email = request.POST.get('email')
        print(email)
        if form.is_valid():
            print('hi')
            user = form.save(commit=False)
            user.username = user.email
            user.first_name = user.email
            user.save()

            messages.success(request,'User account created!')
            login(request,user)
            profile = request.user.profile
            profile.pin_number = request.POST.get('pin_number')
            profile.name = request.POST.get('email')
            print(profile)
            profile.save()
            return redirect('projects')

        else:
            try:
                user = User.objects.get(email=email)
                messages.error(request,'email already exists')
            except User.DoesNotExist:
                return HttpResponse(email)
    # context = {'page':page,'form':form}
    return redirect('projects')


# def generateOTP() :
#      digits = "0123456789"
#      OTP = ""
#      for i in range(4) :
#          OTP += digits[math.floor(random.random() * 10)]
#      return OTP

# def send_otp(request):
#      email=request.POST.get("email")
#      print(email)
#      o=generateOTP()
#      htmlgen = '<p>Your OTP is <strong></strong></p>'
#      send_mail('OTP request',o,'<vertualbazaar gmail id>',[email], fail_silently=False, html_message=htmlgen +o)
#      return HttpResponse(o)