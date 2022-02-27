import json
from django.core import paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from users.models import Profile
from django.contrib import messages
from users.utils import searchProfiles
from .models import Project, Tag,Review,Like
from .forms import ProjectForm,ReviewForm
from .utils import searchProjects ,paginateProjects
from users.forms import CustomUserCreationForm
from urllib.parse import quote

def projects(request):
    try:
        sess = request.COOKIES['sessionid']
    except:
         sess = request.COOKIES['sessionid']=None
    print(request.COOKIES['sessionid'])    
    projects , search_query,search_query1 = searchProjects(request)
    #custom_range, projects = paginateProjects(request,projects,30)
    profile= request.user
    

    context = {
       'projects':projects,
       'search_query':search_query,
       'paginator':paginator,
       #'custom_range':custom_range,
       'user':profile,
       'sess':sess
      
    }

    return render(request, 'projects/projects.html',context)

def project(request,pk):
    print(request.POST)
    lst2=[]
    if request.user.is_authenticated:
        profile= request.user.profile
        pin = profile.pin_number
        all_profile = Profile.objects.filter(pin_number=pin)
        lst=[]
        
        for item in all_profile:
            projects = item.project_set.all()
            
            print(projects)
        
            for obj in projects:
                most_like = obj.liked.count()
                lst.append(most_like)
        
        for item in all_profile:
            projects = item.project_set.all()
            if len(lst) > 0:
                most_liked_project = projects.filter(count=max(lst))
                print(most_liked_project)
                if most_liked_project:
                    
                    for item in most_liked_project:
                        cntx = {}
                        cntx['title'] = item.title
                        cntx['count'] = item.count
                        cntx['image'] = item.featured_image.url,
                        lst2.append(item) 
                else:
                    pass
            print(lst2)
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = projectObj.tags.all()
    #total = Review.objects.filter(project=projectObj).count()
    up = Review.objects.filter(project=projectObj,value='up').count()
    print(up)
    down = Review.objects.filter(project=projectObj,value='down').count()
    s=projectObj.vote_total = up+down
    print(s)
    total = up+down+1
    projectObj.vote_ratio = up
    
    try:
        ratio = up/total
        projectObj.percentage= str(ratio *100)
        projectObj.save()
    except ZeroDivisionError:
        ratio = 0
        projectObj.percentage= str(ratio *100)
        projectObj.save()
   

    if request.method=="POST" :
        if request.user.is_authenticated:
            if request.POST.get("operation") == "like_submit" :
                project_id=request.POST.get("content_id",None)
                project=get_object_or_404(Project,pk=project_id)
                user = request.user.profile
                print('hi',project)
                if user in project.liked.all():
                    project.liked.remove(user)
                    liked=False
                    project.count = project.liked.count()
                    project.save()
                else:
                    project.liked.add(user)
                    print('go')
                    liked=True
                    project.count = project.liked.count()
                    project.save()
               
                ctx={"likes_count":project.liked.count(),"liked":liked,"content_id":project_id}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

    contents=Project.objects.all()
    already_liked=[]
    id=request.user.id
    for content in contents:
        if(content.liked.filter(id=id).exists()):
            already_liked.append(content.id)
    ctx={"contents":contents,"already_liked":already_liked}

    if request.method == 'POST':
    
        try:
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            messages.success(request,'Your review is successfully posted')
        
        #return redirect('project' ,pk=projectObj.id)
        except:
         messages.error(request,'Your review is already posted')
    return render(request, 'projects/single_projects.html',{'project':projectObj,'form':form,'ratio':ratio,'total':total,"contents":contents,"already_liked":already_liked,'cont': lst2})

@login_required(login_url="login")
def createProject(request):
    print(request.POST)
    tag = request.POST.get('tags')
    print(tag)
    profile = request.user.profile
    form = ProjectForm()
    print('p',profile)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            if tag:
                project.tags.add(tag)
            return redirect('account')

        print(request.POST)
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def updateProject(request,pk):
    print(request.POST)
    chked=request.POST.get('check')
    print(chked)
    profile = request.user.profile
  
    project = profile.project_set.get(id=pk)
    print(project.title)
    form = ProjectForm(instance = project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,instance = project)
        if form.is_valid():
            form.save()
            return redirect('account')

       
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {'object':project}
    return render(request,'delete_template.html',context)

def updateStatus(request):
    if request.is_ajax and request.user.is_authenticated:
        profile = request.user.profile
        pk = request.POST.get('project_id')
        status = request.POST.get('state')
        print(request.POST)
        print(pk)
        print(status)
        project = profile.project_set.get(id=pk)
        if status=='true':
            status = True
            project.check = status
            project.save()
        if status=='false':
            status = False
            project.check = status
            project.save()

    return JsonResponse({'msg':'successful'})


def aboutUs(request):
    return render(request,'aboutus.html')