from .models import Project,Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from users.models import Profile ,Skill

def paginateProjects(request, projects,results):

    page = request.GET.get('page')
 
    paginator = Paginator(projects,results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page =1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page))

    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page))

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1
    
    custom_range = range(leftIndex, rightIndex)

    return custom_range , projects


def searchProjects(request):
    search_query =''
    search_query1=''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        search_query1 = request.GET.get('search_query1')
    tags = Tag.objects.filter(name__icontains = search_query)

    proj = Project.objects.distinct().filter(title__icontains = search_query,owner__pin_number__icontains = search_query1)
    print(proj)
    projects = proj.extra(order_by = ['-count'])
    # projects = Project.objects.distinct().filter(
    #         Q(title__icontains = search_query)|
           
    #         Q(description__icontains = search_query)|
    #         Q(owner__name__icontains = search_query)|
    #         Q(tags__in = tags))
    
    print(search_query,search_query1)
    return projects, search_query,search_query1