from login_regapp.models import Userreg
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .forms import ImageForm

import bcrypt

# Create your views here.
#validations 
def regandlogin(request):
    imageupload = ImageForm()
    context ={
        "user_reg" : Userreg.objects.all(),
        "upload" : imageupload
    }


    request.session["logged"] = 0
    return render(request, "regpage.html", context)

def registration(request):
    errors = Userreg.objects.basic_validation(request.POST)
    if len(errors) > 0:          
        for key, value in errors.items():
            messages.error(request, value)
            
        return redirect("/")
    else:   
        user = Userreg.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            region = request.POST['region'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
        
        request.session["image"] = img_obj
        request.session["name"] =  user.first_name
        request.session["email"] = user.email
        print(user.password)
        request.session["logged"] = 1
        return redirect('/pass')

def login(request):
    count = 0
    context ={
        "log-in" : Userreg.objects.all()
    }
    user = Userreg.objects.filter(email = request.POST['email'])
    errors2 = Userreg.objects.basic_login(request.POST)
    if len(errors2) > 0:          
        for key, value in errors2.items():
            messages.error(request, value)            
        return redirect("/")
    request.session["logged"] = 1
    request.session["name"] = user[0].first_name
    request.session["email"] = user[0].email
    # request.session["last_name"] = request.POST['last_name']
    
    return redirect('/pass')

def logout(request):
    request.session.clear()
    return redirect("/")

def inpage(request): 
    id = Userreg.objects.filter(email = request.session["email"])
    form = ImageForm(request.POST, request.FILES)
    image =  request.session["image"]
    id2 = id[0]    
    context ={
        "identifier" : id2,
        "tobeduel" : Userreg.objects.all()
    }
    if request.session["logged"] != 1:
        return redirect('/')
    
    return render(request, "pass.html", context, {'form': form, 'image': image})

def duel(request, id):
    player = Userreg.objects.filter(email = request.session["email"])
    playerid = player[0]
    context ={
    "opponnet" : Userreg.objects.get(id=id),
    "player" : playerid
    }
    return render (request, "duel.html", context)


def duel_elo(request):
    if request.method == "POST":
        #fetching info
        player_id = request.POST["player_id"]
        opponent_id = request.POST["opponnet_id"]
        score_player  = request.POST["score_player"]
        score_opponent  = request.POST["score_opponnet"]
        #player and opponte list objects
        player_info = Userreg.objects.get(id=int(player_id))
        opponent_info = Userreg.objects.get(id=int(opponent_id))

        if int(score_player) > int(score_opponent):
            diference =  player_info.elo - opponent_info.elo 
            if diference > 500: 
                player_info.elo = player_info.elo + 100
                opponent_info.elo  = opponent_info.elo - 100
            else :
                player_info.elo = player_info.elo + 200
                opponent_info.elo  = opponent_info.elo - 200
                
            player_info.save()
            opponent_info.save()
        
        if int(score_player) < int(score_opponent):
            diference =  player_info.elo - opponent_info.elo 
            if diference > 500: 
                player_info.elo = player_info.elo - 300
                opponent_info.elo  = opponent_info.elo + 300
            else :
                player_info.elo = player_info.elo - 200
                opponent_info.elo  = opponent_info.elo + 200
                
            player_info.save()
            opponent_info.save() 

    return redirect("/pass")

def Rank_region(request):
    if request.method == "POST":
        if request.POST["l_region"] == "":
            sorted_ranks = Userreg.objects.all().order_by('-elo')
            context = {
            "ranks" : sorted_ranks            
            }
            return render (request, "ranks.html", context) 
        else:
            location_of_region = request.POST["l_region"]
            sorted_ranks = Userreg.objects.filter(region=location_of_region).order_by('-elo')
            context = {
                "ranks" : sorted_ranks,
                "searched_region" : location_of_region
            }
        return render (request, "ranks.html", context) 



def delete(request, id):
    destroy = Userreg.objects.get(id=id)
    destroy.delete()
    return redirect("/pass")
