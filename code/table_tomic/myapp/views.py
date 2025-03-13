from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player

from .utilities import user as user_utils
from .utilities import match as match_utils

def home(request):
    return render(request,"home.html")

def wip(request):
    return render(request,"wip.html")

@csrf_exempt
def add_user(request):
    if request.method == "POST":
        form = request.POST.dict()
        print(form)
        
        if user_utils.add_new_user(form):
            return HttpResponse("<script>alert('User added successfully!'); window.location='/add_user/';</script>")
        else:
            return HttpResponse("<script>alert('Error adding user!'); window.location='/add_user/';</script>")

    else: # GET
        context = {}
    return render(request,"add_user_form.html",context)


# Create your views here.
def result(request):
    if request.method == "POST":
        form = request.POST.dict()
        print(form)

        outcome = match_utils.manage_match(form) 

        if outcome is False:
            return HttpResponse("<script>alert('Error managing match!'); window.location='/';</script>")

        else:
            return render(request,"result.html",outcome)
        

def ranking(request):

    players = Player.objects.all().order_by('tomic_level').reverse()
    print(players)

    for player in players:
        print(player.name,player.tomic_level)

    context = {'players': players}

    return render(request,"ranking.html",context)

def about(request):
    return render(request,"about.html")