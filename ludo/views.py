from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

def game(request, room_code):
    context = {
        "room_code": room_code,
        }
    return render(request, "game.html", context)

def index(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        return redirect('/ludo/game/%s'%(room_code))
    return render(request, "index.html", {})

@login_required
def game_page(request):
        return render(request , 'game.html')

# def home_page(request):
#         if request.method == 'POST':
#                 room_code = request.POST.get('room_code')
#                 alert(room_code)
#         return render(request , 'home.html')