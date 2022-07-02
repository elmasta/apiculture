from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import *

def index(request):
    return render(request, 'blog/index.html')

def forum(request):
    return render(request, 'blog/index.html')

def shop(request):
    return render(request, 'blog/index.html')

def cours(request, cours_id):
    current_cours = Cours.objects.get(id=cours_id)
    context = {"cours" : current_cours}
    print(context)
    return render(request, 'blog/cours.html', context)

def cours_index(request):
    
    # if request.user.is_authenticated:
    #     if request.method == "POST":
    #         None
    # return redirect("index")
    cours = Cours.objects.all()
    context = {"list" : cours}
    return render(request, 'blog/cours_index.html', context)